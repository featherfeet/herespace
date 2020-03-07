// Vue.js component for a klass editor (an SVG-based editor that displays and optional edits a klass layout).
Vue.component("klass-editor", {
    // The data section is for variables internal to the component.
    data: function() {
        return {
            seatings: [], // This is used to store Seating objects from server_api.js.
            grabbed_seating_index: -1, // This is used to store the index (in the seatings array) of the Seating object currently being dragged-and-dropped.
            selected_seating_index: -1 // This is used to store the index (in the seatings array) of the Seating object currently selected.
        }
    },
    // These props are parameters set on the klass editor by the page that uses it (via Vue.js bindings).
    props: {
        klass_id: Number, // The id of the klass being edited/viewed.
        editable: Boolean // Whether to allow moving/editing of the klass layout.
    },
    // The methods are functions used to generate parts of the template. They are also used as event handlers.
    methods: {
        // Method to calculate the SVG rotate() command for a given Seating object:
        calculateRotation: function(seating) {
            var angle = seating.desk_angle;
            var center_x = seating.desk_x + seating.desk_width / 2.0;
            var center_y = seating.desk_y + seating.desk_height / 2.0;
            return `rotate(${angle}, ${center_x}, ${center_y})`;
        },
        // Methods for the page that includes this component to interact with the seating layout:
        addSeating: function(seating) {
            this.seatings.push(seating);
            this.selected_seating_index = this.seatings.length - 1;
        },
        getSeatings: function() {
            return this.seatings;
        },
        getSelectedSeating: function() {
            return this.seatings[this.selected_seating_index];
        },
        setSeatings: function(seatings) {
            this.seatings = seatings;
        },
        // Handler methods for user interaction with the seating layout:
        handleDragStart: function(event, seating_index) {
            this.grabbed_seating_index = seating_index;
            this.selected_seating_index = seating_index;
            var grabbed_seating = this.seatings[this.grabbed_seating_index];
            this.grabbed_seating_start_location = { desk_x: grabbed_seating.desk_x,
                                                    desk_y: grabbed_seating.desk_y,
                                                    layerX: event.layerX,
                                                    layerY: event.layerY
                                                  };
        },
        handleDrag: function(event) {
            if (this.grabbed_seating_index >= 0 && this.grabbed_seating_index < this.seatings.length) {
                var grabbed_seating = this.seatings[this.grabbed_seating_index];
                grabbed_seating.desk_x = this.grabbed_seating_start_location.desk_x + (event.layerX - this.grabbed_seating_start_location.layerX);
                grabbed_seating.desk_y = this.grabbed_seating_start_location.desk_y + (event.layerY - this.grabbed_seating_start_location.layerY);
            }
        },
        handleDragEnd: function() {
            this.grabbed_seating_index = -1;
        }
    },
    // This function runs on initialization.
    mounted: function() {
        // JS hackery so that the Vue component object is accessible inside handlers.
        var self = this;
        console.log("mounted");
    },
    // The template defines the actual HTML that this component shows.
    template: `
    <svg width="800" height="800" v-on:mousemove="handleDrag" v-on:mouseup="handleDragEnd">
        <svg v-for="(seating, seating_index) in seatings"
             v-bind:transform="calculateRotation(seating)"
             v-bind:x="seating.desk_x"
             v-bind:y="seating.desk_y"
             v-bind:width="seating.desk_width"
             v-bind:height="seating.desk_height">
                <rect x="0"
                      y="0"
                      v-if="seating_index == selected_seating_index"
                      style="fill: white; stroke-width: 5; stroke: red;"
                      v-bind:width="seating.desk_width"
                      v-bind:height="seating.desk_height"
                      v-on:mousedown="handleDragStart($event, seating_index)"
                      rx="15"
                />
                <rect x="0"
                      y="0"
                      v-else
                      style="fill: white; stroke-width: 5; stroke: #3b5998;"
                      v-bind:width="seating.desk_width"
                      v-bind:height="seating.desk_height"
                      v-on:mousedown="handleDragStart($event, seating_index)"
                      rx="15"
                />
                <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" pointer-events="none">{{ seating.student_schedule.student.student_name }}</text>
         </svg>
    </svg>
    `
});
