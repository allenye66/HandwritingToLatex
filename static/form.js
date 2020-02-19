$(document).ready(function() {

    $('form').on('submit', function(event) {

        $.ajax({
            data : {
                text : $('#uri').val()
            },
            type : 'POST',
            url : '/process'
        })

            .done(function(data) {

                if (data.error) {
                    $('#errorAlert').text(data.error).show();
                    $('#succssAlert').hide();
                } else {
                    $('#successAlert').text(data.name).show();
                    $('#errorAlert').hide();
                }

            });

        event.preventDefault();

    });

});