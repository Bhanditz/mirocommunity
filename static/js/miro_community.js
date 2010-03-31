function setup_submit_callbacks(wrap, result) {
    page = $(result);
    if (page.filter('#next').length) {
        location.href = page.filter('#next').attr('href');
        return;
    }
    function callback(result){setup_submit_callbacks(wrap, result);}
    form = wrap.getContent().find('.contentWrap').html(result).find('form:eq(0)');
    form.ajaxForm(callback).find('button').click(function(){form.ajaxSubmit(callback);});
}

$(document).ready( function(){
    $("#nav li").mouseover(function(){$(this).addClass('sfhover');}).mouseout(function(){$(this).removeClass('sfhover');}).filter('.categories a:eq(0)').click(function() {return false;}).css('cursor', 'default');
    $('a[rel^=#]').overlay({
        expose: '#499ad9',
        effect: 'apple',

        onBeforeLoad: function() {
            if (this.getTrigger().attr("href") != "#") {
                wrap = this;
                $.get(this.getTrigger().attr("href"),
                      function(result){setup_submit_callbacks(wrap, result);});
            }
        }
    });
    $("#login form input").live('focus', function() {
        if ($(this).val() == $(this)[0].defaultValue) {
            $(this).val("");
        }
    }).live('blur', function() {
        if ($(this).val() === "") {
            $(this).val($(this)[0].defaultValue);
        }
    });
    $("#login .tabs li a").live('click', function() {
        This = $(this);
        Parent = This.parent();
        Class = This.attr("class");
        if (Class !== "") {
            $("#login .tabs_content > div:visible").hide(500);
            $("#login .tabs_content > div#"+Class).show(500);
            $("#login .tabs li.active").removeClass("active");
            Parent.addClass("active");
        }
        return false;
    });
}).ajaxStart(function() {
    indicator = $("#load-indicator");
    if (!indicator.length) {
        return;
    }
    if ((!indicator.queue().length)) {
	indicator.animate({bottom: 0}, 'fast');
    }
}).ajaxStop(function() {
    $("#load-indicator").stop().css('bottom', '-30px');
});
