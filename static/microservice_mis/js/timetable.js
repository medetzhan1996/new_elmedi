//Получить csrf токен 
var csrftoken = Cookies.get('csrftoken');
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});
//Получить график работы пациента
$(document).on('change', '#select-doctor, #month', function() {
	$('#scheduleDoctorContent').removeClass('hidden')
	var output = ''
	var doctor = $('#select-doctor').val()
	var month = $('#month').val()
  	$.ajax({
      	headers: { "X-CSRFToken": csrftoken },
        url: "/timetable/getData",
        type: 'post',
        data:{
          'doctor': doctor,
          'month': month

        },
        error: function(jqXHR, textStatus, errorThrown) {
          alert(jqXHR.responseText)
        },
        success: function (data) {
          	var returnedData = JSON.parse(data)
          	output+='<table  class="table table-condensed table-responsive table-bordered">'
          	$.each(returnedData, function(key, value){
          		time = value.time ? value.time : ''
          		output += '<tr>'
          		output += '<td>'+time+'</td>'
          		$.each(value.dates, function(key, value2){
          			date = value2.date
          			type = value2.type
		          	dateTime = JSON.stringify({'date': date, 'time': time})
          			content = ''
          			if(time==''){
          				var dateFormat = new Date(date)
          				content = '<td>' + dateFormat.getDate() + '</td>'
          			}
          			else{
          				if(type=='single'){
          					title = 'Пациент: '+value2.patient+'\nДоктор: '+value2.doctor+'\nДата: '+date+'\nВремя: '+time
          					content += '<td class="background-color-red" title="'+title+'">'
          					content += '<input name="scheduleDateTime" type="checkbox" value=\''+dateTime+'\'>'
          					content += '</td>'
          				}
          				else if(type=='double'){
          					content = '<td class="unselectable" title="Пациент: '+value2.patient+'\nДоктор: '+value2.doctor+'">&#10004;</td>'
          				}
          				else{
          					content += '<td class="schedule-td" title="Дата: '+date+'\nВремя: '+time+'">'
          					content += '<input class="hidden" name="scheduleDateTime" type="checkbox" value=\''+dateTime+'\'>'
          					content += '</td>'
          				}
          				
          			}
          			output += content
          		})
          		output += '</tr>'
        	})
        	output+='</table>'
        	$('#timetable-content').html(output)
        }
    })
});
$(document).on('click', '.schedule-td', function() {
  var checkbox=$(this).find(":checkbox:eq(0)");
  if(checkbox.length>0){
    if (checkbox.is(':checked')) {
      checkbox.prop( "checked", false );
      $(this).removeClass('background-color-blue');
    }
    else{
      checkbox.prop( "checked", true );      
      $(this).addClass('background-color-blue');
    } 
  }
});
//Удалить запись из графика работы врача
$(document).on('click', '.delete-schedule', function(e) {
  	e.stopPropagation();
  	var id=$(this).data('id');
  	var _this=$(this);
  	if(confirm('Подтвердите действие!')){
	  	$.ajax({
	      	headers: { "X-CSRFToken": csrftoken },
	        url: "/timetable/deleteData",
	        type: 'post',
	        data:{
	          'id': id
	        },
	        error: function(jqXHR, textStatus, errorThrown) {
	          alert(jqXHR.responseText)
	        },
	        success: function (data) {
	        	_this.closest('div').remove();
	        }
	    })
 	}
});