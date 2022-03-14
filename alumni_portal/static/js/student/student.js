$(document).on('submit','#create_request',function(e) {
    $('#addFinancialRequest').modal('hide');
    
    e.preventDefault();
    const financial_request_form = new FormData($('#create_request')[0]);
    $.ajax({
        type : 'POST',
        url : '/request/create-finance-post/',
        data : financial_request_form,
        processData:false,
        contentType:false,
        success : function(response){
            $('#finance_request_container').html(response.html);
            swal({
                title: "Add Financial",
                text: "Financial Request Added",
                icon: "success",
                closeOnClickOutside: false,
                buttons: {
                    cancel: {
                        text: "Cancel",
                        value: false,
                        visible: true,
                        closeModal: true,
                    },
                    confirm: {
                        text: "ok",
                        value: true,
                        visible: true,
                        closeModal: true
                    }
                }
            });
            // console.log("Hello");
            // console.log(response);
            // $('#create_request')[0].reset();
        },
        error : function(s) {
            console.log(s);
        }
    });
});