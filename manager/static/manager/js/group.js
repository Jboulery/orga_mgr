$('#group-create-button').click(function(e){
    $('#group-name-field').val('');
    $('#group-operation-type-field').val('create');
});

$('#group-update-button').click(function(e){
    $('#group-name-field').val($('#current-active-group').text());
    $('#group-operation-type-field').val('update');
});

$(document).ready(function(){
    $('.group-wrapper').draggable({
        containment: '#page-content-wrapper',
        revert: true,
        zIndex: 1000,
        cursorAt:{
            top: 5,
            left: 5,
        },
    });
    $('.person-wrapper').draggable({
        containment: '#page-content-wrapper',
        revert: true,
        zIndex: 1000,
        cursorAt:{
            top: 5,
            left: 5,
        },
    })
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