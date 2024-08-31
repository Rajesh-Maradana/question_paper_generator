$(document).ready(function() {
    $('#loginf').on('submit', function(event) {
        event.preventDefault();
        var formData = $(this).serializeArray();
        var data= {};
        $.each(formData, function() {
            data[this.name] = this.value;
        });
        $.ajax({
            type: 'POST',
            url: '/login', 
            contentType: 'application/json', 
            data: JSON.stringify(data),
            success: function(response) {
                if (response.status === 'success') {
                    window.location.href = response.redirect_to; 
                }
            },
            error: function(xhr, status, error,response) {
                var errorMessage = xhr.responseJSON.message;
                $('#errorAlert').text(errorMessage).show();
                $('#loginf')[0].reset();
                    setTimeout(function() {
                        $('#errorAlert').fadeOut();
                    }, 3000);     
            }
        });
    });
});


$(document).ready(function() {
    $('#logout_f').on('click', function(event) {
        event.preventDefault();
        console.log()
        $.ajax({
            type: 'POST',
            url: '/logout', 
            contentType: 'application/json', 
            success: function(response) {
                if (response.status === 'success') {
                    console.log(response)
                    window.location.href = "/"; 
                }
            },
            error: function(xhr, status, error,response) {
                var errorMessage = xhr.responseJSON.message;
                $('#errorAlert').text(errorMessage).show();

    
            }
        });
    });
});

// Add
$(document).ready(function() {
    $('#create_question').on('submit', function(event) {
        event.preventDefault();
        var formData = $(this).serializeArray();
        var data= {};
        $.each(formData, function() {
            data[this.name] = this.value;
        });
        $.ajax({
            type: 'POST',
            url: '/create', 
            contentType: 'application/json', 
            data: JSON.stringify(data),
            success: function(response) {
                if (response.status === 'success') {
                    $('#successrAlert').text("Added Successfully").show();
                    $('#create_question')[0].reset();
                    setTimeout(function() {
                        $('#successrAlert').fadeOut();
                    }, 3000); 
                }
            },
            error: function(xhr, status, error,response) {
                var errorMessage = xhr.responseJSON.message;
                $('#errorAlert').text(errorMessage).show();

    
            }
        });
    });
});

// Show
$(document).ready(function() {
    $('#show_question').click(function(event) {
        event.preventDefault();

        $.ajax({
            type: 'GET',
            url: '/show', 
            dataType: 'json',
            success: function(response) {
                if (response.status === 'success') {
                    var table = $('#show_q tbody');
                    table.empty();
                    id=1
                    $.each(response.data, function(index, item) {
                        
                            // table.append("<tr><td>"+item.id+"</td><td>"+item.question+"</td> <td>"+item.subject+"</td><td>"+item.branch+"</td><td>"+item.semester+"</td><td>"+item.difficulty+"</td><td>"+item.marks+"</td><td>"+item.date+"</td></tr>");
                       
                        var row = $('<tr>').attr('id', 'row-' + item.id).append(
                            $('<td>').text(id++),
                            $('<td>').text(item.question),
                            $('<td>').text(item.subject),
                            $('<td>').text(item.branch),
                            $('<td>').text(item.semester),
                            $('<td>').text(item.difficulty),
                            $('<td>').text(item.marks),
                            $('<td>').text(item.date),
                            $('<td>').append("<button class='btn btn-danger' id='delete_btn-"+item.id+"' onclick=del("+item.id+")>Remove</button>") 
                        );
                        table.append(row);
                    }); 
                   
                    $('#show_modal').modal('show');
                    $('#show_q').DataTable({
                        "pageLength": 5
                     });
                    
                }
            },
            error: function(xhr, status, error,response) {
                var errorMessage = xhr.responseJSON.message;
                $('#errorAlert').text(errorMessage).show();

    
            }
        });
    });
});

// Remove


function del(id) {	
    // var row = $(this).closest('tr');
    var q_id=id;
    $.ajax({
        type:'POST',
        url:'/delete',
        data:{id:q_id},
        success:function(response){
            $('#row-'+q_id).remove();
            // alert(response);
        }
    })
 }


 $(document).ready(function() {
    $('#upload_file').on('submit', function(event) {
        event.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            type: 'POST',
            url: '/create', 
            contentType: false,
            processData: false,
            data: formData,
            success: function(response) {
                if (response.status === 'success') {
                    $('#successrAlert').text("Upload Successfully").show();
                    $('#upload_file')[0].reset();
                    setTimeout(function() {
                        $('#successrAlert').fadeOut();
                    }, 3000); 
                }
            },
            error: function(xhr, status, error,response) {
                var errorMessage = xhr.responseJSON.message;
                $('#errorAlert').text(errorMessage).show();

    
            }
        });
    });
});

$(document).ready(function() {
    $('#generate_paper').on('submit', function(event) {
        event.preventDefault();
        var formData = $(this).serializeArray();
        var data= {};
        $.each(formData, function() {
            data[this.name] = this.value;
        });
        $.ajax({
            type: 'POST',
            url: '/generate', 
            contentType: 'application/json', 
            data: JSON.stringify(data),
            success: function(response) {
                if (response.status === 'success') {
                    $('#successrAlertg').text('Generated Successfully').show();
                    $('#generate_paper')[0].reset();
                    setTimeout(function() {
                        $('#successrAlertg').fadeOut();
                    }, 3000); 
                }

            },
            error: function(xhr, status, error,response) {
                var errorMessage = xhr.responseJSON.message;
                $('#errorAlert').text(errorMessage).show();

    
            }
        });
    });
});