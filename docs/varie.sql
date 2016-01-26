
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
