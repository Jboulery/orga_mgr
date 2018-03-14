// Modals display
$('#group-create-button').click(function(e){
    $('#group-name-field').val('');
    $('#group-operation-type-field').val('create');
    $('#update-modal-selected-group-id').val($('#current-active-group, #current-organization').first().data('group-id'));
});

//Groups and persons selection
$('.group-wrapper, .person-wrapper').click(function(e){
    e.preventDefault();
    $(this).toggleClass('active');
    $('#to-delete-entities-names').remove();
    $('#entities-delete-modal-body').append("<ul id='to-delete-entities-names'></ul>")
    var entities_id_list = {'groups': [], 'persons': []}
    $('.group-wrapper.active, .person-wrapper.active').each(function(){
        if($(this).data('type') == 'group'){
            entities_id_list.groups.push($(this).data('entity-id'));
            $('#to-delete-entities-names').append("<li>" + $(this).find('.group-name-wrapper').first().text() + "</li>")
        }
        else if ($(this).data('type') == 'person'){
            entities_id_list.persons.push($(this).data('entity-id'));
            $('#to-delete-entities-names').append("<li>" + $(this).find('.person-name-wrapper').first().text() + "</li>")
        }
    });
    $('#to-delete-entities-field').val(JSON.stringify(entities_id_list));
    if ($('.group-wrapper.active, .person-wrapper.active').length == 0){
        $('#group-delete-button').remove();
        $('#group-update-button').remove();
    }
    else if($('.group-wrapper.active, .person-wrapper.active').length == 1){
        $('#group-delete-button').remove();
        $('#group-update-button').remove();
        if($('.group-wrapper.active').length == 1){
            //Action buttons creation
            $('#tree-path-actions').append("<a id='group-update-button' type='button' data-toggle='modal' data-target='#groupModal' href=''><i class='fas fa-pencil-alt'></i></a>&nbsp;");
            $('#tree-path-actions').append("<a id='group-delete-button' type='button' data-toggle='modal' data-target='#groupDeleteModal' href=''><i class='fas fa-trash-alt'></i></a>");
            //In case of an update of the selected group name
            $('#group-name-field').val($.trim($('.group-wrapper.active').find('.group-name-wrapper').first().text()));
            $('#update-modal-selected-group-id').val($('.group-wrapper.active').first().data('entity-id'));
            $('#group-operation-type-field').val('update');
        }
        else{
            $('#tree-path-actions').append("<a id='group-delete-button' type='button' data-toggle='modal' data-target='#groupDeleteModal' href=''><i class='fas fa-trash-alt'></i></a>");
        }
    }
    else{
        $('#group-update-button').remove();
    }
});

$(document).ready(function(){
    //Drag and drop functions
    $('.group-wrapper, .person-wrapper').draggable({
        containment: '#page-content-wrapper',
        revert: function(){
            $(this).toggleClass('active');
            return true;
        },
        zIndex: 1000,
        cursorAt:{
            top: 5,
            left: 5,
        },
    });
    $('.group-wrapper').droppable({
        drop: function(e, ui){
            var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
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
            $.ajax({
                url: $('#groups-wrapper').data('moveto'),
                data: {
                    entity: $(ui.draggable).data('type'),
                    entity_id: $(ui.draggable).data('entity-id'),
                    target_id: $(this).data('entity-id'),
                },
                type: 'POST',
                dataType: 'json',
                success: function (data) {
                    if(data.success == true){
                        location.reload(true);
                    }
                }
            });
        },
        hoverClass: 'drag-ui-hover-wrapper',
        tolerance: 'pointer',
    });
    $('#current-active-group').droppable({
        drop: function(e, ui){
            e.preventDefault();
            var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
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
            $.ajax({
                url: $('#groups-wrapper').data('moveto'),
                data: {
                    entity: $(ui.draggable).data('type'),
                    entity_id: $(ui.draggable).data('entity-id'),
                    target_id: $(this).data('entity-id'),
                },
                type: 'POST',
                dataType: 'json',
                success: function (data) {
                    if(data.success == true){
                        location.reload(true);
                    }
                }
            });
        },
        hoverClass: 'drag-ui-hover-parent',
        tolerance: 'pointer',
    });
});