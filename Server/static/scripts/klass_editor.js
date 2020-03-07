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
    // The methods are functions used to generate parts of the template. They are also used as event handlers.
    methods: {
        calculateRotation: function(seating) {
            var angle = seating.desk_angle;
            var center_x = seating.desk_x + seating.desk_width / 2.0;
            var center_y = seating.desk_y + seating.desk_height / 2.0;
            return `rotate(${angle}, ${center_x}, ${center_y})`;
        },
        addSeating: function(seating) {
            this.seatings.push(seating);
        },
        getSeatings: function() {
            return this.seatings;
        },
        setSeatings: function(seatings) {
            this.seatings = seatings;
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
    <svg width="800" height="800">
        <svg v-for="seating in seatings"
             v-bind:transform="calculateRotation(seating)"
             v-bind:x="seating.desk_x"
             v-bind:y="seating.desk_y"
             v-bind:width="seating.desk_width"
             v-bind:height="seating.desk_height">
                <rect x="0"
                      y="0"
                      v-bind:width="seating.desk_width"
                      v-bind:height="seating.desk_height"
                      style="fill: none; stroke-width: 5; stroke: #3b5998"
                      rx="15"
                />
                <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle">{{ seating.student_schedule.student.student_name }}</text>
         </svg>
    </svg>
    `
});
