//Получить csrf токен 
/*var csrftoken = Cookies.get('csrftoken');
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
});*/

// Поиск пациента
/*$(document).on('input', '#search', function(){
  var searchText = $(this).val()
  var beginDate = $('#beginDate').val()
  var endDate = $('#endDate').val()
  var output = ''
  var url = '/recorded/'
 $.ajax({
    headers: { "X-CSRFToken": csrftoken },
    url: url,
    type: 'GET',
    data:{
      'searchText': searchText,
      'beginDate': beginDate,
      'endDate': endDate
    },
    error: function(jqXHR, textStatus, errorThrown) {
      alert(jqXHR.responseText)
    },
    success: function (data) {
      $('#recorded-content').html(data)
    }
  })
})*/
/*$(document).on('change', '#beginDate, #endDate', function(){
  var searchParams = new URLSearchParams(window.location.search);
  var beginDate = $('#beginDate').val()
  var endDate = $('#endDate').val()
  searchParams.set('beginDate',beginDate)
  searchParams.set('endDate',endDate)
  var newParams = searchParams.toString()
  window.location.href = window.location.pathname + "?"+newParams;
})*/

/*$(document).on('click', '.appointDoctor', function(e) {
  var id = $(this).data('id')
  $('#appointPatient').val(id)
  $('#contentAppointDoctor').modal('show')
})/*
