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
$(document).on('input', '#searchPatient', function(e) {
	var output=''
	var searchText = $(this).val()
	$('#patientDatalist option').filter(function(){
		if($(this).val() === searchText){
			  var searchParams = new URLSearchParams(window.location.search);
			  searchParams.set('searchText',searchText)
			  var newParams = searchParams.toString()
			  window.location.href = window.location.pathname + "?"+newParams;
		}
	})
	$.ajax({
      	headers: { "X-CSRFToken": csrftoken },
        url: "/patient/search",
        type: 'post',
        data:{
          'searchText': searchText
        },
        error: function(jqXHR, textStatus, errorThrown) {
          alert(jqXHR.responseText)
        },
        success: function (data) {
        	var returnedData = JSON.parse(data)
      		$.each(returnedData, function(key, value){
	       		full_name=value.fields.secondName+' '+value.fields.firstName
				output+="<option value='"+full_name+"'>"
			})
	      	$('#patientDatalist').html(output)
        }
    })
});
//Вывести список пациентов соответствующих критериям поиска
/*$(document).on('input', '#surname,#firstname,#patronymic,#iin', function(){
	var user_text = $(this).val()
  	var list = $(this).attr('list','patientDatalist')
  	var surname = $('#surname').val().trim()
  	var firstname = $('#firstname').val().trim()
  	var patronymic = $('#patronymic').val().trim()
  	var iin = $('#iin').val().trim()
	var output=''
	var selectPatient = $('#patientDatalist option').filter(function(){
		return $(this).val() === user_text
	})
	var patientId=selectPatient.data('id')
	if(patientId){
		var data = selectPatient.data('data')
		$('#surname').val(data.secondName)
		$('#firstname').val(data.firstName)
		$('#birthday').val(data.birthDate)
		$('#sex').append('<option value="'+data.sex+'">'+data.sex+'</option>')
		$('#iin').val(data.iin)
		$('#address').val(data.address)
		$('#place_work').val(data.placeWork)
		$('#profession').val(data.profession)
		$('#telephone_number').val(data.telephoneNumber)
		$('#type_reception').val(data.typeRecorded)
		$('#selectedPatientContent').removeClass('hidden')
		$('#selectedPatient').html(data.secondName+' '+data.firstName)
		$('#update-patient-id').val(patientId)
	}
	else{
		$.ajax({
			headers: { "X-CSRFToken": csrftoken },
		    url: "/patient/search",
		    type: 'POST',
		    data:{
		      'secondName': surname,
		      'firstName':firstname,
		      'iin':iin
		    },
		    error: function(jqXHR, textStatus, errorThrown) {
		      alert(jqXHR.responseText)
		    },
		    success: function (data) {
		    	var returnedData = JSON.parse(data)
	      		$.each(returnedData, function(key, value){
		       		full_name=value.fields.secondName+' '+value.fields.firstName
					output+="<option data-data='"+JSON.stringify(value.fields)+"' data-id='"+value.pk+"' value='"+full_name+"'>"
				})
		      	$('#patientDatalist').html(output)
		    }
	  	})
	}
})*/

//Очистить ранее введенные данные пациента
$(document).on('click', '#clearPatientData', function(){
	event.preventDefault()
	$('#savePatientData')[0].reset()
	$('#selectedPatientContent').addClass('hidden')
	$('#update-patient-id').val('')
})

//Извлечь данные пациента для редактирования
$(document).on('click', '.update-patient', function(){
	patientId = $(this).data('id')
	$.ajax({
		headers: { "X-CSRFToken": csrftoken },
	    url: "/patient/search",
	    type: 'POST',
	    data:{
	      'patientId': patientId
	    },
	    error: function(jqXHR, textStatus, errorThrown) {
	      alert(jqXHR.responseText)
	    },
	    success: function (data) {
	    	var returnedData = JSON.parse(data)
	    	$.each(returnedData, function(key, value){
		      	$('#surname').val(value.fields.secondName)
				$('#firstname').val(value.fields.firstName)
				$('#birthday').val(value.fields.birthDate)
				$('#sex').append('<option value="'+value.fields.sex+'">'+value.fields.sex+'</option>')
				$('#iin').val(value.fields.iin)
				$('#address').val(value.fields.address)
				$('#place_work').val(value.fields.placeWork)
				$('#profession').val(value.fields.profession)
				$('#telephone_number').val(value.fields.telephoneNumber)
				$('#type_reception').val(value.fields.typeRecorded)
				$('#selectedPatientContent').removeClass('hidden')
				$('#selectedPatient').html(value.fields.secondName+' '+value.fields.firstName)
				$('#update-patient-id').val(value.pk)
			})
	    }
	  })
})

//Искать пациента
$(document).on('click', '#search-patient', function(){
	var iin = $('#iin').val()
	event.preventDefault()
	$.ajax({
		headers: { "X-CSRFToken": csrftoken },
	    url: "/patient/search",
	    type: 'POST',
	    data:{
	      'iin':iin
	    },
	    error: function(jqXHR, textStatus, errorThrown) {
	      alert(jqXHR.responseText)
	    },
	    success: function (data) {
	    	var returnedData = JSON.parse(data)
      		$.each(returnedData, function(key, value){
		      	$('#surname').val(value.fields.secondName)
				$('#firstname').val(value.fields.firstName)
				$('#birthday').val(value.fields.birthDate)
				$('#sex').append('<option value="'+value.fields.sex+'">'+value.fields.sex+'</option>')
				$('#iin').val(value.fields.iin)
				$('#address').val(value.fields.address)
				$('#place_work').val(value.fields.placeWork)
				$('#profession').val(value.fields.profession)
				$('#telephone_number').val(value.fields.telephoneNumber)
				$('#type_reception').val(value.fields.typeRecorded)
				$('#selectedPatientContent').removeClass('hidden')
				$('#selectedPatient').html(value.fields.secondName+' '+value.fields.firstName)
				$('#update-patient-id').val(value.pk)
			})
	    }
  	})
	$.ajax({
		headers: { "X-CSRFToken": csrftoken },
	    url: "/insurance/getInsuranceStatus",
	    type: 'POST',
	    data:{
	      'iin': iin
	    },
	    error: function(jqXHR, textStatus, errorThrown) {
	      alert(jqXHR.responseText)
	    },
	    success: function (data) {
	    	$('#insurance-content').html(data)
	    }
	  })
})
