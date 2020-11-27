/**
 * @version 1
 */

function editActivity(id) {
    alert('You click edit action, id: ' + id)
}

function removeActivity(id) {
    alert('You click remove action, id: ' + id)
}

function operateFormatter(value, row, index) {
    return [
        '<a class="edit" href="#" onclick="editActivity(' + index + ')" title="Edit">',
        '<i class="fa fa-pen"></i>',
        '</a>  ',
        '<a class="remove" href="#" onclick="removeActivity(' + index + ')" title="Remove">',
        '<i class="fa fa-trash"></i>',
        '</a>'
    ].join('')
}

function initPersonalActivities(id) {
    console.log('Init Personal Activities: ' + id);

    let $table = $(id);
    $table.bootstrapTable('destroy').bootstrapTable({
        columns: [{
            title: 'Date',
            field: 'datetime',
            align: 'center'
        }, {
            title: 'Distance',
            field: 'distance',
            align: 'right'
        }, {
            title: 'Duration',
            field: 'duration',
            align: 'center'
        }, {
            title: '',
            field: 'operate',
            align: 'center',
            clickToSelect: false,
            formatter: operateFormatter
        }]
    });
}
