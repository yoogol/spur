$(document).ready(function() {
    $('.datepicker').datepicker();
})

function manageTask(task_id, type, status, onSuccess) {
    $.ajax({
        url: '/api/manage_task/',
        data: {
            'type': type,
            'task_id': task_id,
            'status': status
        },
        dataType: 'json',
        success: function (data) {
            onSuccess(data)
        }
    });
}

function deleteTask(task_id) {
    manageTask(task_id, 'change_status', 'D', onSuccess)
    function onSuccess(data) {
        if(data.hasOwnProperty('redirect_url')) {
            location.replace(data['redirect_url'])
        } else {
            console.log("NO")
        }

    }
}

function changeTaskStatus(el) {
    let status = ''
    let task_id = $(el).attr('data-taskid')
    if (el.checked) {
        status = 'C'
    } else {
        status = 'A'
    }
    function onSuccess(data) {
        let selector = "#" + task_id
        if (el.checked) {
            $(selector).children('.title').children('span').css('text-decoration','line-through')
        } else {
            $(selector).children('.title').children('span').css('text-decoration','')
        }
    }
    manageTask(task_id, 'change_status', status, onSuccess)
}