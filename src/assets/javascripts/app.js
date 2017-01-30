!(function () {
  'use strict';

  var tableShowHide = {
    selector: '.table-show-hide ',

    init: function(params) {
      var that = this;
      $.each($(this.selector), function(index, showHide) {
        var rows = $(showHide).find('table tr');
        rows.each(function() {
          if ($(this).index() >= params.rowLimit) {
            $(this).hide();
          }
        });
        if (rows.length > params.rowLimit) {
          $(showHide).find('a.toggle')
            .on('click', params, that.callback)
            .show();
        }
      });
    },

    callback: function(event) {
      var a = $(this);
      var rows = $(this).parents('section').first().find('tr');
      a.toggleClass('expanded');
      if (a.hasClass('expanded')) {
        a.text('Close');
        rows.show();
      } else {
        a.text('Show all');
        rows.each(function(i) {
          if ($(this).index() >= event.data.rowLimit) $(this).hide();
        });
      }
    }
  };

  var typeAhead = {
    options: {
      hint: true,
      highlight: true,
      minLength: 3,
      classNames: {
        input: 'form-control tt-input',
        hint: 'form-control tt-hint'
      }
    },

    sourceOptions: {
      name: 'states',
      source: new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote: {
          url: '/api/locations?q=%QUERY',
          wildcard: '%QUERY'
        }
      })
    },

    // what to do when the first 'Add another area' button is clicked
    add1: function() {
      $(this).hide();
      $('#location2, #add2, #del1, #del2').show();
    },

    // what to do when the second 'Add another area' button is clicked
    add2: function() {
      $(this).hide();
      $('#location3, #add2, #del2, #del3').show();
    },

    // what to do when the first 'Remove' button is clicked
    del1: function() {
      // we've remove the first location, copy the 2 others down
      $('#id_location1').val($('#id_location2').val());
      $('#id_location2').val($('#id_location3').val());

      // second location field disappears if not third present
      if (!$('#location3').is(':visible')) {
        $('#location2').hide();
        $('#add1').show();
        $('#add2').hide();
      } else {
        $('#add2').show();
      }
      if (!$('#location2').is(':visible')) {
        $('#del1').hide();
      }
      $('#location3').val('').hide();
    },

    // second Remove button is clicked
    del2: function() {
      $('#id_location2').val($('#id_location3').val());
      $('#id_location3').val('');
      if (!$('#location3').is(':visible')) {
        $('#location2, #add2, #del1, #del2').hide();
        $('#add1').show();
      } else {
        $('#add2').show();
      }
      $('#location3').hide();
    },

    del3: function() {
      $('#id_location3').val('');
      $('#location3').hide();
      $('#add2').show();
    },

    init: function(params) {
      if ($('#id_location2').val()) {
        $('#add1').hide();
        $('#location2, #add2, #del2').show();
      } else {
        $('#add1').show();
        $('#location2').hide();
      }

      if ($('#id_location3').val()) {
        $('#add2').hide();
        $('#location3, #del3').show();
      } else {
        $('#location3').hide();
      }

      $('#add1').on('click', this.add1);
      $('#add2').on('click', this.add2);
      $('#del1').on('click', this.del1);
      $('#del2').on('click', this.del2);
      $('#del3').on('click', this.del3);

      $(params.selector).typeahead(this.options, this.sourceOptions);
    },
  };


  $(document).ready(function() {
    tableShowHide.init({ rowLimit: 3});
    typeAhead.init({ selector: '.location-input' });
  });

})();
