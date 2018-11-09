/**
 * Manages the direction of the scroll.
 */
$(document).ready(function () {
    /**
     * This object controls the navigation bar. Implement the add and remove
     * action over the elements of the navbar that we want to change.
     *
     * @type {{flagAdd: boolean, elements: string[], add: Function, remove: Function}}
     */
    var navbar = {
        flagAdd: true,
        elements: [],
        init: function (elements) {
            this.elements = elements;
        },
        add: function () {
            if (this.flagAdd) {
                for (var i = 0; i < this.elements.length; i++) {
                    document.getElementById(this.elements[i]).className += " fixed-theme";
                }
                this.flagAdd = false;
            }
        },
        remove: function () {
            for (var i = 0; i < this.elements.length; i++) {
                document.getElementById(this.elements[i]).className =
                    document.getElementById(this.elements[i]).className.replace(/(?:^|\s)fixed-theme(?!\S)/g, '');
            }
            this.flagAdd = true;
        }
    };

    /**
     * Initializes the object. Pass the object the array of elements
     * that we want to change when the scroll goes down.
     */
    navbar.init([
        "navbar-menu"
    ]);

    /**
     * Function that manage the direction of the scroll.
     */
    function offSetManager() {
        var yOffset = 0;
        var currYOffSet = window.pageYOffset;

        if (yOffset < currYOffSet) {
            navbar.add();
        } else if (currYOffSet === yOffset) {
            navbar.remove();
        }
    }

    /**
     * Binds to the document scroll detection.
     */
    window.onscroll = function () {
        offSetManager();
    };

    /**
     * We have to do a first detectation of offset because the page
     * could be load with scroll down set.
     */
    offSetManager();
});

/**
 * Sets footer fixed in bottom if page height is less or equals of window height.
 */
if ($(document).height() <= $(window).height()) {
    $("footer.footer").addClass("fixed-bottom");
}
