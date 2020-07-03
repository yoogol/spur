$(document).ready(function() {
    $('.datepicker').datepicker();
})

function manageTask(task_id, type, status, onSuccess) {
    console.log(status)
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

function manageProject(project_id, type, status, onSuccess) {
    $.ajax({
        url: '/api/manage_project',
        data: {
            'type': type,
            'project_id': project_id,
            'status':status
        },
        dataType: 'json',
        success: function(data) {
            onSuccess(data)
        }
    });
}

function deleteProject(project_id) {
    manageProject(project_id, 'change_status', 'D', onSuccess)
    function onSuccess(data) {
        if(data.hasOwnProperty('redirect_url')) {
            location.replace(data['redirect_url'])
        } else {
            console.log("NO")
        }
    }
}

function changeTaskStatus(el) {
    let checkedStatus = $(el).hasClass('checked')
    if (checkedStatus) {
        status = 'A'
    } else {
        status = 'C'
    }
    console.log(status)
    let task_id = $(el).attr('data-taskid')
    function onSuccess(data) {
        let selector = "#" + task_id
        console.log($(selector))
        console.log($(selector).find('.task-name'))
        if (status == 'C') {
            $(selector).find('.task-name').css('text-decoration','line-through')
            $(selector).find('.unchecked').removeClass('fa-square-o').removeClass('unchecked').addClass('fa-check-square-o').addClass('checked')
        } else {
            $(selector).find('.task-name').css('text-decoration','')
            $(selector).find('.checked').removeClass('fa-check-square-o').removeClass('checked').addClass('fa-square-o').addClass('unchecked')
        }
    }
    manageTask(task_id, 'change_status', status, onSuccess)
}