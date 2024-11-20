$(document).on("blur","span[contenteditable=true]",function() {  
  var marker_id='#'+$(this).data('editable');  
  var text = $(this).text().replace(new RegExp('↵', 'g'),'<br/>');  
  $(marker_id).val(text);
})

//Скрыть окно готовых шаблонов при нажатии вне фокуса 
$(document).on("click","body",function(e) { 
    $('.ready-phrase').each(function () {
      if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
        $(this).popover('hide')
      }
    })
})

//Добавить готовые фразы
$(document).on('click', '.phrase-add', function() {
	event.preventDefault();
	var phrase_add = $('#phrase-add').html()
	$('#phrase-add-content').append(phrase_add)
})

$(document).on("click",".ready-phrase",function() { 
	var marker_id = $(this).data('id')
  	var _this = $(this);
  	$('#save-ready-phrases').val(marker_id)
  	$.ajax({
	    headers: { "X-CSRFToken": csrftoken },
	    url: '/form/getReadyPhrase',
	    type: 'POST',
	    data:{
	      	'marker': marker_id
	    },
	    error: function(jqXHR, textStatus, errorThrown) {
	      alert(jqXHR.responseText)
	    },
	    success: function (data) {
	      	_this.popover({
	        	placement: 'bottom',
	        	title: 'Вставка шаблонов <span style="float:right;" class="phrase-add">&#43;</span>',
	        	html:true,
	        	content:  function(){
	          		return data;
	        	}
	      	});
	    }
	})
})

//Сохранить готовые фразы
$(document).on('click', '#save-ready-phrases', function() {
	event.preventDefault()
	var ready_phrase_value = $('#ready-phrase-select').val()
    var marker_id = $(this).val();
    $('#'+marker_id).val(ready_phrase_value)
    $('span[data-editable="'+marker_id+'"]').append(ready_phrase_value)
    var phrase = $('input[name="phrase"]').map(function(){ return this.value;}).get()
    var phrase_description = $('input[name="phrase_description"]').map(function(){ return this.value;}).get()
    if(phrase_description != ''){
    	$.ajax({
		    headers: { "X-CSRFToken": csrftoken },
		    url: '/form/addReadyPhrase',
		    type: 'POST',
		    data: $('#phrase-add-form').serialize()+'&'+$.param({ 'marker': marker_id }),
		    error: function(jqXHR, textStatus, errorThrown) {
		      alert(jqXHR.responseText)
		    },
		    success: function (data) {
		    	$('.popover').hide()
		    }
		})
    }
    else{
    	$('.popover').hide()
    } 
})

// Событие при фокусе contenteditable
$(document).on("focus","span[contenteditable=true]",function() {  
	var selected_marker = $('#selected-marker').val()
	var marker = $(this).data('editable')
	$('#selected-marker').val(marker)
  	var _this = $(this);
  	if(selected_marker != marker){
	  	$.ajax({
		    headers: { "X-CSRFToken": csrftoken },
		    url: '/form/ready/phrase',
		    type: 'GET',
		    data:{
		      	'marker': marker
		    },
		    error: function(jqXHR, textStatus, errorThrown) {
		      alert(jqXHR.responseText)
		    },
		    success: function (data) {
		      	$('#content-ready-phrase').html(data)
		    }
		})
  	}
})

// Выбрать родительскую форму
$(document).on('change', '#parent-form-id', function() {
	var form_id = $(this).val()
	var url = '/form/getMarkers/' + form_id
	$.ajax({
	    headers: { "X-CSRFToken": csrftoken },
	    url: url,
	    type: 'POST',
	    data: {},
	    error: function(jqXHR, textStatus, errorThrown) {
	      alert(jqXHR.responseText)
	    },
	    success: function (data) {
	    	$('#parent-list-markers').html(data)
	    }
	}) 
})

$(document).on('click', '#sendForm', function() {
	event.preventDefault()
	url = '/form/saveParentData'
	$.ajax({
	    headers: { "X-CSRFToken": csrftoken },
	    url: url,
	    type: 'POST',
	    data: $('#save-parent-markers').serialize(),
	    error: function(jqXHR, textStatus, errorThrown) {
	      alert(jqXHR.responseText)
	    },
	    success: function (data) {
	    	var status = $("<input>").attr("type", "hidden").attr("name", "status").val("4")
			$('#saveForm').append(status)
			var sendDoctor = $("<input>").attr("type", "hidden").attr("name", "sendDoctor").val($('#sendDoctor').val())
			$('#saveForm').append(sendDoctor)
			$('#saveForm').submit()
	    }
	})
})

$(document).on("click",".select-phrase",function() { 
	var marker_id = $('#selected-marker').val()
	var description = $(this).data('description') + ' '
	$('#'+marker_id).val(description)
	$('span[data-editable="'+marker_id+'"]').append(description).focus()
	document.execCommand('selectAll', false, null);
	document.getSelection().collapseToEnd();
})

$(document).on("click","#append-phrase",function() {
	var marker_id = $('#selected-marker').val()
	if(marker_id){
		$('#save-phrase').removeClass('hidden')
		var phrase_add = $('#phrase-add').html()
		$('#phrase-add-content').append(phrase_add)
	}

})

$(document).on("click","#save-phrase",function() { 
	var marker_id = $('#selected-marker').val()
	var phrase = $('input[name="phrase"]').map(function(){ return this.value;}).get()
    var phrase_description = $('input[name="phrase_description"]').map(function(){ return this.value;}).get()
    if(phrase_description != ''){
    	$.ajax({
		    headers: { "X-CSRFToken": csrftoken },
		    url: '/form/ready/phrase',
		    type: 'POST',
		    data: $('#phrase-add-form').serialize(),
		    error: function(jqXHR, textStatus, errorThrown) {
		      alert(jqXHR.responseText)
		    },
		    success: function (data) {
		    	$('#selected-marker').val('')
		    	$('span[data-editable="' + marker_id + '"]').focus();
		    	$('#save-phrase').addClass('hidden')
		    	$('#phrase-add-content').html('')
		    }
		})
    }
})



//поиск форм
$(document).on('input', '#search-phrase', function() {
  	var value = $(this).val().toLowerCase();
  	$("#content-ready-phrase tr").filter(function() {
    	$(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
  	});
});

$(document).on("click",".datalist-val",function() {
 	var id = $(this).data('id')
  	event.preventDefault()
  	var val=$("span[data-editable='" + id +"']").append('  '+$(this).find('a').html()).focus()
	document.execCommand('selectAll', false, null);
	document.getSelection().collapseToEnd();
  	$('#'+id).val(val.text())
})
