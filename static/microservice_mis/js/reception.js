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
//поиск форм
$(document).on('input', '#search-form', function() {
  if($(this).val()!=''){
    $('.group-form').each(function () {
      $('.'+$(this).data('id')).removeClass('hidden');
    });
  }
  else{
    $('.group-form').each(function () {
      $('.'+$(this).data('id')).addClass('hidden');
    });
  }
  var value = $(this).val().toLowerCase();
  $("#search-content tr").filter(function() {
    $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
  });
});

$(document).on('click', '.group-form', function() {
  var _class = '.'+$(this).data('id');
  $(_class).toggleClass('hidden');
});

$(document).on('change', '#begin-date, #end-date', function() {
  var begin_date = $('#begin-date').val()
  var end_date = $('#end-date').val()
  var id = $('#patientId').val()
  var url = '/reception/' + id
  $.ajax({
    headers: { "X-CSRFToken": csrftoken },
    url: '/reception/1',
    type: 'GET',
    data:{
      'beginDate': begin_date,
      'endDate': end_date
    },
    error: function(jqXHR, textStatus, errorThrown) {
      alert(jqXHR.responseText)
    },
    success: function (data) {
      $('#list-history-content').html(data)
    }
  })
})