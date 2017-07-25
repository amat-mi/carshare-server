/**
	Seleziona tutti i veicoli che sono stati disponibili al noleggio almeno una volta,
	ma che non hanno autorizzazioni (sono quasi soltanto gli scooter).
	ATTENZIONE!!! In realtà anche gli scooter risultano come "kind"='car'!!!
*/

select
v.*,
a.fromstamp,
a.tostamp,
null as webstamp,
null as daysdiff
from carshare_authorization a
right join carshare_vehicle v using(plate)
where a.plate is null
order by v.agency_id,v.plate;


/**
	Seleziona tutti i veicoli che ma che non hanno autorizzazioni, 
	ma che non sono stati disponibili al noleggio nemmeno una volta.
*/

select
null as id,
a.plate,
null as design,
null as engine,
null as kind,
a.agency_id,
a.fromstamp,
a.tostamp,
null as webstamp,
null as daysdiff
from carshare_authorization a
left join carshare_vehicle v using(plate)
where v.plate is null
order by a.agency_id,a.plate;


/**
	Seleziona i veicoli che sono stati disponibili al noleggio
	in una data antecedente all'inizio della loro autorizzazione
	(non è troppo lenta, circa 50 secondi per 4 record trovati)
*/

select
v.*,
a.fromstamp,
a.tostamp,
d.webstamp,
d.webstamp::date-a.fromstamp as daysdiff
from (
select
d.vehicle_id,
min(d.webstamp) as webstamp
from carshare_vehicledata d
group by d.vehicle_id) d
join carshare_vehicle v on v.id=d.vehicle_id
join carshare_authorization a on a.plate=v.plate
where d.webstamp::date < a.fromstamp
order by a.agency_id,a.plate;


/**
	Seleziona i veicoli che sono stati disponibili al noleggio
	in una data successiva alla fine della loro autorizzazione
	(non è troppo lenta, circa 50 secondi per 23 record trovati)
*/

select
v.*,
a.fromstamp,
a.tostamp,
d.webstamp,
d.webstamp::date-a.tostamp as daysdiff
from (
select
d.vehicle_id,
max(d.webstamp) as webstamp
from carshare_vehicledata d
group by d.vehicle_id) d
join carshare_vehicle v on v.id=d.vehicle_id
join carshare_authorization a on a.plate=v.plate
where d.webstamp::date > a.tostamp
order by a.agency_id,a.plate;


/**
	Crea VIEW per avere tutte le autorizzazioni CAR2GO, sia 2013, sia 2016
*/

CREATE OR REPLACE VIEW "CAR2GO_tElencoTarghe" as 
select
t13."Targa" as plate,
'2013-01-01'::date as fromstamp,
t13."Scadenza" as tostamp,
4 as agency_id
from "CAR2GO_tElencoTarghe_2013" t13
left join "CAR2GO_tElencoTarghe_2016" t16 using ("Targa")
where t16."Targa" is null
UNION
select
t16."Targa" as plate,
t16."Decorrenza" as fromstamp,
t16."Scadenza" as tostamp,
4 as agency_id
from "CAR2GO_tElencoTarghe_2013" t13
right join "CAR2GO_tElencoTarghe_2016" t16 using ("Targa")
where t13."Targa" is null
UNION
select
t13."Targa" as plate,
'2013-01-01' as fromstamp,
t16."Scadenza" as tostamp,
4 as agency_id
from "CAR2GO_tElencoTarghe_2013" t13
join "CAR2GO_tElencoTarghe_2016" t16 using ("Targa");


/**
	Crea VIEW per avere tutte le autorizzazioni ENI, sia 2013, sia 2016
*/

CREATE OR REPLACE VIEW "ENI_tElencoTarghe" as 
select
t13."Targa" as plate,
t13."DecorrenzaPass" as fromstamp,
t13."Scadenza" as tostamp,
2 as agency_id
from "ENI_tElencoTarghe_2013" t13
left join "ENI_tElencoTarghe_2016" t16 using ("Targa")
where t16."Targa" is null
UNION
select
t16."Targa" as plate,
t16."Decorrenza" as fromstamp,
t16."Scadenza" as tostamp,
2 as agency_id
from "ENI_tElencoTarghe_2013" t13
right join "ENI_tElencoTarghe_2016" t16 using ("Targa")
where t13."Targa" is null
UNION
select
t13."Targa" as plate,
coalesce(t13."DecorrenzaPass",'2013-01-01'::date) as fromstamp,
t16."Scadenza" as tostamp,
2 as agency_id
from "ENI_tElencoTarghe_2013" t13
join "ENI_tElencoTarghe_2016" t16 using ("Targa");


/**
	Aggiorna la tabella finale delle autorizzazioni impostando il campo "tostamp"
	in base al cambio targa, ove non già impostato (per i veicoli Car2Go)
*/

UPDATE carshare_authorization
set tostamp=(select t16."Decorrenza"
	from "CAR2GO_tElencoTarghe_2013" t13
	join "CAR2GO_tElencoTarghe_2016" t16 on t16."Targa"=replace("CambioTarga",'Sostituita da ','')
	where t13."Targa"=carshare_authorization.plate)
where tostamp is null;


/**
	Aggiorna la tabella finale delle autorizzazioni impostando il campo "tostamp"
	in base al cambio targa, ove non già impostato (per i veicoli ENI)
*/

UPDATE carshare_authorization
set tostamp=(select t16."Decorrenza"
	from "ENI_tElencoTarghe_2013" t13
	join "ENI_tElencoTarghe_2016" t16 on t16."Targa"=replace("CambioTarga",'Sostituita da ','')
	where t13."Targa"=carshare_authorization.plate)
where tostamp is null;


---------------------------------------------------------
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
