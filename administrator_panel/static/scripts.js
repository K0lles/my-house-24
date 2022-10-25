$('tr[data-href]').not('button').on('click', function() {
    document.location = $(this).data('href');
});