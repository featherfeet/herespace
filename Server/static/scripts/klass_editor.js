// Calculate distance between two points.
function distance(x1, y1, x2, y2) {
    return Math.hypot(x2 - x1, y2 - y1);
}

class KlassEditor {
    initializeCanvasContextWithDPI(width, height) {
        var devicePixelRatio = window.devicePixelRatio || 1;
        this.devicePixelRatio = devicePixelRatio;
        console.log(`this.devicePixelRatio: ${this.devicePixelRatio}`);
        this.canvas_element.width = width * devicePixelRatio;
        this.canvas_element.height = height * devicePixelRatio;
        this.canvas_element.style.width = `${width}px`;
        this.canvas_element.style.height = `${height}px`;
        this.ctx = this.canvas_element.getContext("2d");
        this.ctx.scale(devicePixelRatio, devicePixelRatio);
        this.redraw();
    }

    handleDragStart(event) {
        var self = event.data;

        for (var i = 0; i < self.seatings.length; i++) {
            var seating = self.seatings[i];
            if (seating.containsPoint(event.offsetX, event.offsetY)) {
                self.grabbed_seating_offset_x = event.offsetX - seating.desk_x;
                self.grabbed_seating_offset_y = event.offsetY - seating.desk_y;
                self.grabbed_seating = i;
                self.selected_seating = i;
                self.rotate_seating_slider.value = seating.desk_angle * (180.0 / Math.PI);
                break;
            }
        }

        self.redraw();
    }

    handleDrag(event) {
        var self = event.data;

        if (self.grabbed_seating != -1) {
            self.seatings[self.grabbed_seating].desk_x = event.offsetX - self.grabbed_seating_offset_x;
            self.seatings[self.grabbed_seating].desk_y = event.offsetY - self.grabbed_seating_offset_y;
            self.redraw();
        }
    }

    handleDragEnd(event) {
        var self = event.data;

        self.grabbed_seating = -1;
    }

    handleRotateSeating(event) {
        var self = event.data;

        self.seatings[self.selected_seating].desk_angle = parseFloat(self.rotate_seating_slider.value) * Math.PI / 180.0;
        self.redraw();
    }

    initializeCanvasHandlers() {
        $(this.canvas_element).on("mousedown", null, this, this.handleDragStart);
        $(this.canvas_element).on("mousemove", null, this, this.handleDrag);
        $(this.canvas_element).on("mouseup", null, this, this.handleDragEnd);
    }

    constructor(canvas_element, rotate_seating_slider) {
        // Array of all seatings (Seating objects) being displayed.
        this.seatings = new Array();
        // The index (in the this.seatings array) of the seating currently being drag-and-dropped.
        this.grabbed_seating = -1;
        // The index (in the this.seatings array) of the seating currently selected (for editing).
        this.selected_seating = -1;
        // The offset distance in pixels of the mouse when it grabbed a seating. This is used so that the seating does not "jump" locations  to align its center with the mouse.
        this.grabbed_seating_offset_x = 0;
        this.grabbed_seating_offset_y = 0;
        // The HTML5 <canvas> element.
        this.canvas_element = canvas_element;
        // The slider (<input type="range">) used to rotate seats.
        this.rotate_seating_slider = rotate_seating_slider;
        this.rotate_seating_slider.min = -180.0;
        this.rotate_seating_slider.max = 180.0;
        this.rotate_seating_slider.step = 1.0;
        this.rotate_seating_slider.value = 0.0;
        $(this.rotate_seating_slider).on("input", null, this, this.handleRotateSeating);
        // Used to calculate clicks and scalings for HiDPI displays.
        this.devicePixelRatio = 1.0;
        // Initialize the canvas for HiDPI displays.
        this.initializeCanvasContextWithDPI(800, 800);
        // Initialize the mouse interaction handlers for the canvas.
        this.initializeCanvasHandlers();
    }

    addSeating(seating) {
        this.seatings.push(seating);
        this.redraw();
    }

    redraw(event) {
        console.log("Redrawing...");
        // JS hackery to allow redraw() to be used as a JQuery event callback with the KlassEditor object passed as "event.data".
        var self = null;
        if (event == null) {
            self = this;
        }
        else {
            self = event.data;
        }
        // Clear the canvas.
        self.ctx.clearRect(0, 0, self.canvas_element.width, self.canvas_element.height);

        // Draw the seats that have already been placed.
        for (var i = 0; i < self.seatings.length; i++) {
            // Save the transformation state of the canvas.
            self.ctx.save();
            // Find the center point of the seat being drawn.
            var seating = self.seatings[i];
            var seating_center_x = seating.desk_x + seating.desk_width / 2.0;
            var seating_center_y = seating.desk_y + seating.desk_height / 2.0;
            // Translate the canvas to the center point of the seat being drawn.
            self.ctx.translate(seating_center_x, seating_center_y);
            // Rotate the canvas.
            self.ctx.rotate(seating.desk_angle);
            // Translate the canvas back to its original location.
            self.ctx.translate(-seating_center_x, -seating_center_y);
            // Draw the seat.
            if (i == self.selected_seating) {
                self.ctx.strokeStyle = "red";
            }
            else {
                self.ctx.strokeStyle = "#3b5998";
            }
            self.ctx.lineWidth = 3;
            self.ctx.strokeRect(seating.desk_x, seating.desk_y, seating.desk_width, seating.desk_height);
            self.ctx.font = "14pt Verdana";
            self.ctx.textAlign = "center";
            self.ctx.textBaseline = "middle";
            self.ctx.fillText(seating.student_schedule.student.student_name, seating_center_x, seating_center_y);
            // Restore the transformation state of the canvas.
            self.ctx.restore();
        }
    }
}
