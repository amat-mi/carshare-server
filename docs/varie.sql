
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
	Calcola il numero di campioni presenti in ogni intervallo di 5 minuti.
	ATTENZIONE!!! Ignora eventuali campioni con i minuti di "stamp" non allineati
 	ai 5 minuti, ma non dovrebbero essercene!!!
*/

select
d.stamp::date,
extract(hour from d.stamp) as hour,
s.m as minute,
count(*)
from carshare_vehicledata d
join (select generate_series(2,57,5) as m) s on s.m=extract(minute from d.stamp)
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
