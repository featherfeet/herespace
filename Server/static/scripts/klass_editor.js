// Vue.js component for a klass editor (an SVG-based editor that displays and optional edits a klass layout).
Vue.component("klass-editor", {
    // The data section is for variables internal to the component.
    data: function() {
        return {
            seatings: [] // This is used to store Seating objects from server_api.js.
        }
    },
    // These props are parameters set on the klass editor by the page that uses it (via Vue.js bindings).
    props: {
        klass_id: Number, // The id of the klass being edited/viewed.
        editable: Boolean // Whether to allow moving/editing of the klass layout.
    },
    // This function runs on initialization.
    mounted: function() {
        // JS hackery so that the Vue component object is accessible inside handlers.
        var self = this;
        console.log("mounted");

        // If the klass_id is -1, we are creating a new klass, so don't try to fetch it.
        if (self.$props.klass_id == -1) {
            return;
        }

        // Retrieve seatings from the server and put them into this.seatings so that they can be displayed.
        retrieveSeatings(self.$props.klass_id).then(function(seatings) {
            self.seatings = seatings;
            // Calculate where the seatings should be displayed within the SVG and save the result into the Seating objects.
            for (var i = 0; i < self.seatings.length; i++) {
                var angle = self.seatings[i].desk_angle;
                var center_x = self.seatings[i].desk_x + self.seatings[i].desk_width / 2.0;
                var center_y = self.seatings[i].desk_y + self.seatings[i].desk_height / 2.0;
                var transformation = `rotate(${angle}, ${center_x}, ${center_y})`;
                self.seatings[i].setAttribute("transformation", transformation);
            }
        });
    },
    // The template defines the actual HTML that this component shows.
    template: `<svg>
        <g v-for="seating in seatings"
           :key="seating.seating_id"
           v-bind:transform="seating.transformation"
           width="800"
           height="800">

        </g>
    </svg>`
})
