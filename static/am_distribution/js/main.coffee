get_url_parameter = (name) ->
    decodeURIComponent(
        (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search) or [null, null])[1]
    )
    
$ ->
    $(".media_group").colorbox({rel: 'media_group', maxWidth: '700px', maxHeight: '700px'});

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

    $('#download_all_version_type_btn').on 'click', (e) ->
        $('#overlay').show()
        $('#download_all_version_type').show()

    $('#overlay, #download_all_version_type a').on 'click', (e) ->
        $('#overlay').hide()
        $('#download_all_version_type').hide()

                