const app = new Vue(
    {
        el: "#vue_div",
        data: {
            klass_editor: null,
            klass_id: -1
        },
        methods: {

        },
        mounted: function() {
            var self = this;

            const raw_url = window.location.href;
            const url = new URL(raw_url);
            self.klass_id = parseInt(url.searchParams.get("klass_id"));

            var canvas = $("canvas")[0];
            self.klass_editor = new KlassEditor(canvas, null, false);

            retrieveSeatings(self.klass_id).then(function(seatings) {
                self.klass_editor.setSeatings(seatings);
            });
        }
    }
);
