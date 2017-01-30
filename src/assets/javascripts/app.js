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
            $(this).attr('aria-hidden', 'true').hide();
          }
        });
        if (rows.length > params.rowLimit) {
          $(showHide).find('a.toggle')
            .on('click', params, that.callback)
            .attr('aria-hidden', 'false').show();
        }
      });
    },

    callback: function(event) {
      var a = $(this);
      var rows = $(this).parents('section').first().find('tr');
      a.toggleClass('expanded');
      if (a.hasClass('expanded')) {
        a.text('Close');
        rows.attr('aria-hidden', 'false').show();
      } else {
        a.text('Show all');
        rows.each(function(i) {
          if ($(this).index() >= event.data.rowLimit) $(this).attr('aria-hidden', 'true').hide();
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
      $(this).attr('aria-hidden', 'true').hide();
      $('#location2, #add2, #del1, #del2').attr('aria-hidden', 'false').show();
    },

    // what to do when the second 'Add another area' button is clicked
    add2: function() {
      $(this).attr('aria-hidden', 'true').hide();
      $('#location3, #add2, #del2, #del3').attr('aria-hidden', 'false').show();
    },

    // what to do when the first 'Remove' button is clicked
    del1: function() {
      // we've remove the first location, copy the 2 others down
      $('#id_location1').val($('#id_location2').val());
      $('#id_location2').val($('#id_location3').val());

      // second location field disappears if not third present
      if (!$('#location3').is(':visible')) {
        $('#location2').attr('aria-hidden', 'true').hide();
        $('#add1').attr('aria-hidden', 'false').show();
        $('#add2').attr('aria-hidden', 'true').hide();
      } else {
        $('#add2').attr('aria-hidden', 'false').show();
      }
      if (!$('#location2').is(':visible')) {
        $('#del1').attr('aria-hidden', 'true').hide();
      }
      $('#location3').val('').attr('aria-hidden', 'true').hide();
    },

    // second Remove button is clicked
    del2: function() {
      $('#id_location2').val($('#id_location3').val());
      $('#id_location3').val('');
      if (!$('#location3').is(':visible')) {
        $('#location2, #add2, #del1, #del2').attr('aria-hidden', 'true').hide();
        $('#add1').attr('aria-hidden', 'false').show();
      } else {
        $('#add2').attr('aria-hidden', 'false').show();
      }
      $('#location3').attr('aria-hidden', 'true').hide();
    },

    del3: function() {
      $('#id_location3').val('');
      $('#location3').attr('aria-hidden', 'true').hide();
      $('#add2').attr('aria-hidden', 'false').show();
    },

    init: function(params) {
      if ($('#id_location2').val()) {
        $('#add1').attr('aria-hidden', 'true').hide();
        $('#location2, #add2, #del2').attr('aria-hidden', 'false').show();
      } else {
        $('#add1').attr('aria-hidden', 'false').show();
        $('#location2').attr('aria-hidden', 'true').hide();
      }

      if ($('#id_location3').val()) {
        $('#add2').attr('aria-hidden', 'true').hide();
        $('#location3, #del3').attr('aria-hidden', 'false').show();
      } else {
        $('#location3').attr('aria-hidden', 'true').hide();
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
