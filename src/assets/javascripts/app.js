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

    init: function(params) {
      $(params.selector).typeahead(this.options, this.sourceOptions);
    },
  };


  $(document).ready(function() {
    tableShowHide.init({ rowLimit: 3});
    typeAhead.init({ selector: '.location_input' });
  });

})();
