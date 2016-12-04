$(document).ready(function(){
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

  $('.vet-status').click(function(){
    if( $(this).hasClass('vet-status--unvetted') ) {
      $(this).removeClass('vet-status--unvetted');
      $(this).addClass('vet-status--vetted');
      $(this).html('<span class="icon-vetted"></span>Vetted');
    } else if ( $(this).hasClass('vet-status--vetted') ) {
      $(this).removeClass('vet-status--vetted');
      $(this).addClass('vet-status--unvetted');
      $(this).html('Unvetted');
    }
  });
});
