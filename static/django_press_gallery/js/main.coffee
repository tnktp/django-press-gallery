get_url_parameter = (name) ->
    decodeURIComponent(
        (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search) or [null, null])[1]
    )
    
$ ->
    $('#login_form').on 'submit', (e) ->
        e.preventDefault()
        $form = $(@)
        url = location.pathname
        data = $form.serialize()

        $.post url, data, (res) ->
            next = get_url_parameter('next')
            next = '/pressphotos' if next is 'null'
            window.location.replace(next)
        .error (xhr, textStatus, errorThrown) ->
            if xhr.status == 400
                $form.find('.error_message').show()
                