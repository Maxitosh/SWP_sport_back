const tour = new Tour({
    framework: "bootstrap4",
    name: 'main-tour',
    showProgressBar: false,
    showProgressText: false,
    backdrop: true,
    debug: true,
    localization: {
        buttonTexts: {
            prevButton: "Back",
            endTourButton: "Finish"
        }
    },
    onEnd: function (tour) {
        // Variable for semester hours
        // There are 3 states:
        // 1) null => not passed, no need to show (e.g. at the very beginning)
        // 2) false => not passed, need to show (e.g. there was no attendance during the tour walkthrough)
        // 3) true => passed, no need to show (e.g. when this step was passed/seen)
        if (localStorage.getItem("main-tour_student_hours") === null) {
            localStorage.setItem("main-tour_student_hours", "false");
        }

        // Variable for calendar
        // The same stages as for the semester hours (above)
        // Do not set variable if the choosing process is going - end() was forced and tour is not finished yet
        if (localStorage.getItem("main-tour_calendar") === null &&
                !(localStorage.getItem("main-tour_choosing_process") === "true")) {
            localStorage.setItem("main-tour_calendar", "false");
        }
    }
});

$(function () {
    // First step
    tour.addStep(
        {
            orphan: true, // Center the popover
            title: "Hello!",
            content: "Welcome to the helpdesk.innopolis.university!<br />" +
                "Here is a small tour to help you navigate the site.",
            path: "/profile/"
        }
    );

    // For trainers
    tour.addStep(
        {
            element: "#trainer-list",
            placement: "bottom",
            title: "Sport Groups",
            content: "It is the list of sports groups you train.",
            path: "/profile/"
        }
    );

    // For students
    tour.addSteps([
        {
            element: "#student-list",
            placement: "bottom",
            title: "Sport Groups",
            content: "You will see here the list of sports groups you joined.",
            path: "/profile/"
        },
        {
            element: "#medical-group",
            placement: "bottom",
            title: "Medical Group",
            content: "Your medical group can be seen here (If you passed medical check up).<br />" +
                "You can click on the ellipse to check out the description.",
            path: "/profile"
        },
        {
            element: "#semester-hours",
            placement: "bottom",
            title: "Attendance",
            content: "You can see all your graded activities in the current semester here.<br />" +
                "Click it to check out the detailed information.",
            path: "/profile",
            onShown: function (tour) {
                // Show only this step in the tour (used in conjunction with restart(4) below)
                if (localStorage.getItem("main-tour_student_hours") === "false") {
                    // Hide prev and next buttons. Edit end button
                    $("button[data-role='prev']").hide();
                    $("button[data-role='next']").hide();
                    $("button[data-role='end']").text("Ok");
                }
            },
            onHide: function (tour) {
                // If modal is open and user clicks on prev or next, or end, modal is closed
                // jQuery - attribute starts with selector [name^='value']
                $("[id^='hours-modal']").modal('hide');
            },
            onHidden: function (tour) {
                // This step has been seen - mark it
                localStorage.setItem("main-tour_student_hours", "true");
            },
            onEnd: function (tour) {
                // If both attendance and calendar steps were skipped, after attendance go to calendar
                if (localStorage.getItem("main-tour_calendar") === "false") {
                    if ($('.tour-step-choice-btn').text().includes('No group choices left')) {
                        // When max number of groups
                        tour.goTo(7);
                    } else {
                        // Otherwise
                        tour.goTo(15);
                    }
                }
            }
        }
    ]);

    /* If there is no such element, the tour will skip the step */
    // If student can enroll
    if (!$(".tour-step-choice-btn.disabled").length || document.URL.includes("/category/")) {
        tour.addSteps([
            {
                element: ".tour-step-choice-btn",
                placement: "bottom",
                reflex: true, // Continue only on button click
                reflexOnly: true,
                title: "Sport Groups",
                content: "Here you can choose your sports group. <strong>Click it!</strong>",
                path: "/profile/",
            },
            {
                orphan: true,
                title: "Sport Groups",
                content: "You can select from three categories - <strong>student clubs</strong>, " +
                    "<strong>university trainers</strong>, and <strong>sport complex trainers</strong>.",
                path: "/category/"
            },
            {
                element: "#tour-step-category-1-landscape",
                placement: "right",
                title: "Student Club",
                content: "Here you can choose your favorite student club where you want to get hours.",
                path: "/category/",
                preventInteraction: true
            },
            {
                element: "#tour-step-category-1-portrait",
                placement: "bottom",
                title: "Student Club",
                content: "Here you can choose your favorite student club where you want to get hours.",
                path: "/category/",
                preventInteraction: true
            },
            {
                element: "#tour-step-category-2-landscape",
                placement: "left",
                title: "IU Trainer",
                content: "Point here if you want to get hours for sports classes that the university offers you.",
                path: "/category/",
                preventInteraction: true
            },
            {
                element: "#tour-step-category-2-portrait",
                placement: "top",
                title: "IU Trainer",
                content: "Point here if you want to get hours for sports classes that university offers you.",
                path: "/category/",
                preventInteraction: true
            },
            {
                element: "#tour-step-category-3-landscape",
                placement: "left",
                title: "SC Trainer",
                content: "Select this if you exercise with sport complex trainers and want to get hours.",
                path: "/category/",
                preventInteraction: true
            },
            {
                element: "#tour-step-category-3-portrait",
                placement: "top",
                title: "SC Trainer",
                content: "Select this if you exercise with sport complex trainers and want to get hours.",
                path: "/category/",
                preventInteraction: true
            },
            {
                orphan: true,
                title: "Sport Groups",
                content: "Now it's time to choose your sports groups for the next semester!<br />" +
                    "<strong>Hover the desired category to choose the group.</strong>",
                path: "/category/",
                localization: {
                    buttonTexts: {
                        nextButton: "Select",
                        endTourButton: "Skip"
                    }
                },
                onNext: function (tour) {
                    localStorage.setItem("main-tour_choosing_process", "true");
                    // Allow to end tour from onNext
                    localStorage.setItem("main-tour_force_end", "true");

                    tour.end();
                },
                onEnd: function (tour) {
                    tour.goTo(tour.getCurrentStepIndex() + 1);
                }
            }
        ]);
    } else {
        // If student cannot enroll
        tour.addStep(
            {
                element: ".tour-step-choice-btn",
                placement: "bottom",
                title: "Sport Groups",
                content: "Here you can choose your sports group.<br />Unfortunately, you have chosen the maximum number of groups. " +
                    "Unenroll to pick a new group.",
                path: "/profile/"
            }
        );
    }

    // Ill button
    tour.addStep(
        {
            element: ".tour-step-ill-btn",
            placement: "bottom",
            title: "Illness",
            content: "If you are ill, press this to inform your trainers.<br />" +
                "Do not forget to change the status back when you recover.<br />" +
                "Additionally, you can submit a reference to get hours.",
            path: "/profile/",
            preventInteraction: true
        }
    );

    /* If calendar is shown on the page */
    // For both students and trainers
    if (document.getElementById("student-span") && document.getElementById("trainer-span")) {
        tour.addStep(
            {
                element: "#calendar",
                placement: "auto",
                title: "Calendar",
                content: "It is your schedule. You can find all your sports classes there.<br />" +
                    "There are <strong>two types of events - with and without the icon.</strong><br /><br />" +
                    "Events <strong>without the icon</strong> are the ones you joined. " +
                    "You can click on the training to check out details such as trainer contacts or location.<br /><br />" +
                    "Events <strong>with the icon</strong> are the ones you train. You can click on the training to mark attendance.",
                path: "/profile/",
                onShown: function (tour) {
                    // Show only calendar steps in the tour (used in conjunction with calendar restart() below)
                    if (localStorage.getItem("main-tour_calendar") === "false") {
                        // Hide prev. Edit end button
                        $("button[data-role='prev']").hide();
                        $("button[data-role='end']").text("Skip");

                        // Required for the next step
                        // Note: code in the onNext is executed after onHide and onHidden,
                        // thus this line cannot be placed in either of two functions
                        localStorage.setItem("main-tour_calendar_btns", "false");
                    }

                    const step = tour.getStep(tour._current);
                    $(step.element)[0].scrollIntoView(false);
                },
                onHidden: function (tour) {
                    // This step has been seen - mark it
                    localStorage.setItem("main-tour_calendar", "true");
                }
            }
        );
    } else {
        // For only trainers
        if (document.getElementById("trainer-span")) {
            tour.addStep(
                {
                    element: "#calendar",
                    placement: "auto",
                    title: "Calendar",
                    content: "It is your schedule. You can find all your sports classes there.<br />" +
                        "You can click on the training to mark attendance.",
                    path: "/profile/",
                    onShown: function (tour) {
                        // Show only calendar steps in the tour (used in conjunction with calendar restart() below)
                        if (localStorage.getItem("main-tour_calendar") === "false") {
                            // Hide prev. Edit end button
                            $("button[data-role='prev']").hide();
                            $("button[data-role='end']").text("Skip");

                            // Required for the next step
                            // Note: code in the onNext is executed after onHide and onHidden,
                            // thus this line cannot be placed in either of two functions
                            localStorage.setItem("main-tour_calendar_btns", "false");
                        }

                        const step = tour.getStep(tour._current);
                        $(step.element)[0].scrollIntoView(false);
                    },
                    onHidden: function (tour) {
                        // This step has been seen - mark it
                        localStorage.setItem("main-tour_calendar", "true");
                    }
                }
            );
        } else {
            // For only students
            if (document.getElementById("student-span")) {
                tour.addStep(
                    {
                        element: "#calendar",
                        placement: "auto",
                        title: "Calendar",
                        content: "It is your schedule. You can find all your sports classes there.<br />" +
                            "You can click on the training to check out details such as trainer contacts or location.",
                        path: "/profile/",
                        onShown: function (tour) {
                            // Show only calendar steps in the tour (used in conjunction with calendar restart() below)
                            if (localStorage.getItem("main-tour_calendar") === "false") {
                                // Hide prev. Edit end button
                                $("button[data-role='prev']").hide();
                                $("button[data-role='end']").text("Skip");

                                // Required for the next step
                                // Note: code in the onNext is executed after onHide and onHidden,
                                // thus this line cannot be placed in either of two functions
                                localStorage.setItem("main-tour_calendar_btns", "false");
                            }

                            const step = tour.getStep(tour._current);
                            $(step.element)[0].scrollIntoView(false);
                        },
                        onHidden: function (tour) {
                            // This step has been seen - mark it
                            localStorage.setItem("main-tour_calendar", "true");
                        }
                    }
                );
            }
        }
    }
    // For all
    tour.addStep(
        {
            element: ".fc-right",
            placement: "top",
            title: "Calendar",
            content: "You can navigate through the calendar using these buttons.",
            path: "/profile/",
            onShown: function (tour) {
                // Show only calendar steps in the tour (can be accessed only from previous step)
                if (localStorage.getItem("main-tour_calendar_btns") === "false") {
                    // Hide next. Edit end button
                    $("button[data-role='next']").hide();
                    $("button[data-role='end']").text("Ok");
                }
            },
            onPrev: function (tour) {
                // Reset variable for the previous step
                if (localStorage.getItem("main-tour_calendar_btns") === "false") {
                    localStorage.setItem("main-tour_calendar", "false");
                }
            }
        }
    );

    // Highlight "?" button
    tour.addStep(
        {
            element: "#help-btn",
            placement: "bottom",
            title: "Help",
            content: "Forgot something? Consider clicking this to repeat the tour.",
            path: "/profile/",
            preventInteraction: true,
            onShown: function (tour) {
                // Stick highlighting to the button
                const highlighter = $("#tourHighlight");
                highlighter.css("top", "");
                highlighter.css("left", "");
                highlighter.css("bottom", "3%");
                highlighter.css("right", "3%");
                highlighter.css("position", "fixed");
            },
            onHidden: function (tour) {
                const highlighter = $("#tourHighlight");
                highlighter.css("bottom", ""); // Reset bottom and right to avoid white spot on the screen during "prev"
                highlighter.css("right", "");
                highlighter.css("position", "absolute");
            }
        }
    );

    // Last step
    tour.addStep(
        {
            orphan: true,
            title: "Thank You!",
            content: "Thank you for your patience! Now you know how to use this site!",
            path: "/profile/"
        }
    );

    /* Starting the tour */

    // On jump to the /profile check if the student was in choosing process
    // If so, depending on their number of groups, jump to the corresponding tour step
    if (document.URL.includes("/profile/") && localStorage.getItem("main-tour_choosing_process") === "true") {
        localStorage.removeItem("main-tour_choosing_process");

        if ($('.tour-step-choice-btn').text().includes('No group choices left')) {
            tour.restart(6);
        } else {
            tour.restart(14);
        }
    } else if (document.URL.includes("/profile/") && document.getElementById("semester-hours") &&
            tour.ended() && localStorage.getItem("main-tour_student_hours") === "false") {
        // Show semester hours for student if it was skipped previously
        tour.restart(4);
    } else if (document.URL.includes("/profile/") && document.getElementById("calendar") &&
            tour.ended() && localStorage.getItem("main-tour_calendar") === "false") {
        // Show calendar steps if it was skipped previously
        if ($('.tour-step-choice-btn').text().includes('No group choices left')) {
            tour.restart(7);
        } else {
            tour.restart(15);
        }
    } else {
        tour.start();
    }
});

function start_tour() {
    if (tour.ended()) {
        tour.restart();
    } else {
        tour.start();
    }
}
