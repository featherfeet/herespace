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
            var canvas = $("canvas")[0];
            this.klass_editor = new KlassEditor(canvas, 0);
        }
    }
);
