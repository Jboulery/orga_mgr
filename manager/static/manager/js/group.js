$('#group-create-button').click(function(e){
    $('#group-name-field').val('');
    $('#group-operation-type-field').val('create');
});

$('#group-update-button').click(function(e){
    $('#group-name-field').val($(this).attr('data-group'));
    $('#group-operation-type-field').val('update');
});