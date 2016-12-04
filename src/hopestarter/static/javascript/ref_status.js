$(document).ready(function(){
	$(document).ajaxSend(function(event, xhr, settings) {
		function getCookie(name) {
			var cookieValue = null;
			if (document.cookie && document.cookie !== '') {
				var cookies = document.cookie.split(';');
				for (var i = 0; i < cookies.length; i++) {
					var cookie = $.trim(cookies[i]);
					// Does this cookie string begin with the name we want?
					if (cookie.substring(0, name.length + 1) == (name + '=')) {
						cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
						break;
					}
				}
			}
			return cookieValue;
		}
		if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
			// Only send the token to relative URLs i.e. locally.
			xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
		}
	});

  $(".vet-form").submit(function(e){
      e.preventDefault();
      var data = {
          "id": $(this).data('user-id')
      }, vet_status = $('.vet-status', this);
      if (vet_status.hasClass('vet-status--vetted')){
        data.status = "unvetted";
      } else if (vet_status.hasClass('vet-status--unvetted')) {
        data.status = "vetted";
      } else {
        console.error("Unknown status!");
        return;
      }

      $.ajax({
        url: $(this).attr('action'),
        type: "POST",
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
      }).done(function(){
          if( vet_status.hasClass('vet-status--unvetted') ) {
            vet_status.removeClass('vet-status--unvetted');
            vet_status.addClass('vet-status--vetted');
            vet_status.html('<span class="icon-vetted"></span>Vetted');
          } else if ( vet_status.hasClass('vet-status--vetted') ) {
            vet_status.removeClass('vet-status--vetted');
            vet_status.addClass('vet-status--unvetted');
            vet_status.html('Unvetted');
          }
      }).fail(function(){
          console.error(this);
      }).always(function(){
          console.log(this);
      });
  });
  $("input[name='tabs']").change(function(){
    var status = $(this).val();
    $('.ref-status--profile').each(function(){
        var profile = this;
        if (status == "any") {
            $(profile).show();
        } else if ($('.vet-status', profile).hasClass('vet-status--'+status)){
            $(profile).show();
        } else {
            $(profile).hide();
        }
    });
  });

});
