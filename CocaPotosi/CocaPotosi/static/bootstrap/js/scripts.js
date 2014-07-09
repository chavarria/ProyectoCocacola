$(function(){
	// alert('OK');
	if (navigator.geolocation)
	{
		navigator.geolocation.getCurrentPosition(getCoords, getError);
	}else{

		initialize(-19.571228999999963, -65.76189451481935);
	}
	function getCoords(position)
	{
		var lat=position.coords.latitude;
		var lng=position.coords.longitude;

		initialize(lat, lng);
	}
	function getError(err)
	{
		initialize(-19.571228999999963, -65.76189451481935);
	}
	function initialize(lat, lng)
	{
		var LatLng= new google.maps.LatLng(lat, lng);
		var mapSettings ={
			center: LatLng,
			zoom: 15,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		}
		map= new google.maps.Map($('#mapa').get(0), mapSettings);

		var marker= new google.maps.Marker({
			position:LatLng,
			map:map,
			draggable: true,
			title: 'Arrastrame'
		});
		google.maps.event.addListener(marker,'position_changed', function(){
			getMarkerCoords(marker);
		});
	}
	function getMarkerCoords(marker)
	{
		var markerCoords= marker.getPosition();
		$('#id_lat').val(markerCoords.lat());
		$('#id_lng').val(markerCoords.lng());
	}
	$('#form_coords').submit(function(e){
		e.preventDefault();
		$.post('/coords/save',$(this).serialize(),function(data){
			if(data.ok)
			{
				$('#data').html(data.msg);
				$('#form_coords').each(function(){ this.reset(); });
			}else{
				alert(data.msg);
			}
		},'json');
	});
});