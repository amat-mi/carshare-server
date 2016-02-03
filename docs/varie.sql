
/**
	Seleziona i dati di tutti i veicoli per i quali ci sono almeno 5 dati,
	ovvero quelli che sono stati noleggiati e rilasciati più volte.
*/

select
*
from carshare_vehicledata d
where d.vehicle_id in (select
vehicle_id
from carshare_vehicledata d
group by vehicle_id
having count(*) >= 5 order by count(*) desc)
order by vehicle_id,stamp;


/**
	Calcola la distanza in metri e in gradi tra due record di dati
	(tipicamente dovrebbero essere due dati consecutivi dello stesso veicolo).
*/

select
st_distance(st_transform(d1.geom,3003),st_transform(d2.geom,3003)),
st_distance(d1.geom,d2.geom),
st_asewkt(d1.geom),st_asewkt(d2.geom),
*
from carshare_vehicledata d1,carshare_vehicledata d2
where d1.id=12105 and d2.id=13267;


/** 
	Calcola il numero di campioni presenti in ogni intervallo di 5 minuti,
	considerando anche quelli non eventualmente allineati ai 5 minuti.
*/

select
d.stamp::date,
extract(hour from d.stamp) as hour,
s.m+2 as minute,
count(*)
from carshare_vehicledata d
join (select generate_series(0,55,5) as m) s on extract(minute from d.stamp) between s.m and s.m+4
group by d.stamp::date,extract(hour from d.stamp),s.m
order by d.stamp::date,extract(hour from d.stamp),s.m;


/**
	Seleziona i campioni con i minuti di "stamp" non allineati ai 5 minuti.
	Non dovrebbero essercene e invece ci sono, ma pochi, a parte i primi campioni
	memorizzati durante i test...
*/

select
*
from carshare_vehicledata d
left join (select generate_series(2,57,5) as m) s on s.m=extract(minute from d.stamp)
where s.m is null
order by stamp desc;


/**
	Crea il dato completo per un certo veicolo in un certo periodo prendendo per ogni intervallo di 5 minuti
	l'ultimo record esistente, anche se con dato non disponibile (veicolo in viaggio).
*/

WITH tick AS (
select
'2016-01-26 20:00:00'::timestamp + (s.m+2 || ' minutes')::interval as stamp,
'2016-01-26 20:00:00'::timestamp + (s.m || ' minutes')::interval as stampfrom,
'2016-01-26 20:00:00'::timestamp + (s.m+5 || ' minutes')::interval as stampto
from (select generate_series(0,(24*60*7)-1,5) as m) s
),
d AS (
select
*,
lead(stamp) OVER (PARTITION BY vehicle_id ORDER BY id) as stampto
from carshare_vehicledata d
)
select
d.*,
ref.stamp as tickstamp
from (
select * from carshare_vehicle v, tick
) ref
left join d on d.vehicle_id=ref.id and 
	(
		(d.stamp>=ref.stampfrom and d.stamp<ref.stampto) or
		(ref.stampfrom>=d.stamp and ref.stampto<d.stampto)
	)
where ref.id=1
order by ref.stampfrom,ref.id;


/**
	Crea una tabella che materializza il dato completo per tutti i veicoli in un certo periodo 
	prendendo per ogni intervallo di 5 minuti l'ultimo record esistente, 
	ma solo se con dato disponibile (veicolo non in viaggio).
	ATTENZIONE!!! E' un po' pesante (circa 4 minuti e mezzo per 2.150.155 record in un periodo di una settimana)!!!
*/

CREATE TABLE carshare_20160127_one_week AS
WITH tick AS (
select
'2016-01-27 00:00:00'::timestamp + (s.m+2 || ' minutes')::interval as stamp,
'2016-01-27 00:00:00'::timestamp + (s.m || ' minutes')::interval as stampfrom,
'2016-01-27 00:00:00'::timestamp + (s.m+5 || ' minutes')::interval as stampto
from (select generate_series(0,(24*60*7)-1,5) as m) s
),
d AS (
select
*,
lead(stamp) OVER (PARTITION BY vehicle_id ORDER BY id) as stampto
from carshare_vehicledata d

)
select
ref.stamp as stamp,
d.vehicle_id,
d.address,
d.fuel,
d.inside,
d.outside,
d.webstamp,
d.geom
from (
select * from carshare_vehicle v, tick
) ref
left join d on d.vehicle_id=ref.id and 
	(
		(d.stamp>=ref.stampfrom and d.stamp<ref.stampto) or
		(ref.stampfrom>=d.stamp and ref.stampto<d.stampto)
	)
where webstamp is not null
order by ref.stampfrom,ref.id;
