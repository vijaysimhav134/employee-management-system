/*
 * Employee Management System - frontend behaviour
 * Vanilla JavaScript, no dependencies, no build step.
 *
 * Handles:
 *  - Mobile sidebar drawer
 *  - Delete confirmation dialog
 *  - Toast notifications (auto-dismiss + close button)
 *  - Currency formatting (Indian digit grouping)
 *  - Today's date in the top bar
 *  - Submit-button loading state
 */
(function () {
    "use strict";

    /* ---------- Sidebar (mobile drawer) ---------- */

    var body = document.body;
    var menuToggle = document.getElementById("menu-toggle");

    function setSidebar(open) {
        body.classList.toggle("sidebar-open", open);
        if (menuToggle) {
            menuToggle.setAttribute("aria-expanded", open ? "true" : "false");
        }
    }

    if (menuToggle) {
        menuToggle.addEventListener("click", function () {
            setSidebar(!body.classList.contains("sidebar-open"));
        });
    }

    document.querySelectorAll("[data-sidebar-close]").forEach(function (el) {
        el.addEventListener("click", function () { setSidebar(false); });
    });

    document.querySelectorAll(".sidebar .nav-link").forEach(function (link) {
        link.addEventListener("click", function () { setSidebar(false); });
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") { setSidebar(false); }
    });


    /* ---------- Toast notifications ---------- */

    function dismissToast(toast) {
        if (!toast || toast.classList.contains("leaving")) { return; }
        toast.classList.add("leaving");
        setTimeout(function () {
            if (toast.parentNode) { toast.parentNode.removeChild(toast); }
        }, 250);
    }

    document.querySelectorAll(".toast").forEach(function (toast) {
        var delay = toast.classList.contains("toast-error") ? 8000 : 5000;
        var timer = setTimeout(function () { dismissToast(toast); }, delay);

        // Pause auto-dismiss while the user is reading it
        toast.addEventListener("mouseenter", function () { clearTimeout(timer); });
        toast.addEventListener("mouseleave", function () {
            timer = setTimeout(function () { dismissToast(toast); }, 2500);
        });

        var close = toast.querySelector(".toast-close");
        if (close) {
            close.addEventListener("click", function () { dismissToast(toast); });
        }
    });


    /* ---------- Delete confirmation dialog ---------- */

    var dialog = document.getElementById("delete-dialog");
    var pendingForm = null;

    if (dialog) {
        var nameSlot = dialog.querySelector("[data-delete-name]");
        var cancelBtn = dialog.querySelector("[data-delete-cancel]");
        var confirmBtn = dialog.querySelector("[data-delete-confirm]");
        var supportsDialog = typeof dialog.showModal === "function";

        document.querySelectorAll(".delete-form").forEach(function (form) {
            form.addEventListener("submit", function (event) {
                var nameInput = form.querySelector('input[name="employee_name"]');
                var employeeName = nameInput ? nameInput.value : "this employee";

                // Very old browsers without <dialog>: fall back to the native prompt
                if (!supportsDialog) {
                    if (!window.confirm("Are you sure you want to delete " + employeeName + "?")) {
                        event.preventDefault();
                    }
                    return;
                }

                event.preventDefault();
                pendingForm = form;
                nameSlot.textContent = employeeName;
                dialog.showModal();
                cancelBtn.focus();
            });
        });

        function closeDialog() {
            pendingForm = null;
            if (dialog.open) { dialog.close(); }
        }

        cancelBtn.addEventListener("click", closeDialog);

        confirmBtn.addEventListener("click", function () {
            var form = pendingForm;
            closeDialog();
            // form.submit() does not re-fire the submit event, so no loop
            if (form) { form.submit(); }
        });

        // Click on the backdrop closes the dialog
        dialog.addEventListener("click", function (event) {
            if (event.target === dialog) { closeDialog(); }
        });

        dialog.addEventListener("close", function () { pendingForm = null; });
    }


    /* ---------- Currency formatting (e.g. ₹12,34,567.00) ---------- */

    document.querySelectorAll("[data-currency]").forEach(function (el) {
        var amount = parseFloat(el.getAttribute("data-currency"));
        if (isNaN(amount)) { return; }

        try {
            el.textContent = "₹" + amount.toLocaleString("en-IN", {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
        } catch (e) {
            /* keep the server-rendered value */
        }
    });


    /* ---------- Today's date ---------- */

    document.querySelectorAll("[data-today]").forEach(function (el) {
        try {
            el.textContent = new Date().toLocaleDateString("en-IN", {
                weekday: "short",
                day: "numeric",
                month: "short",
                year: "numeric"
            });
        } catch (e) {
            el.textContent = new Date().toDateString();
        }
    });


    /* ---------- Submit button loading state ---------- */

    document.querySelectorAll("form[data-loading]").forEach(function (form) {
        form.addEventListener("submit", function () {
            var button = form.querySelector('button[type="submit"]');
            if (!button) { return; }

            // Defer so the browser still submits the form normally
            setTimeout(function () {
                button.classList.add("is-loading");
                button.disabled = true;
            }, 0);
        });
    });

    // Restore buttons if the page is shown again from the back/forward cache
    window.addEventListener("pageshow", function (event) {
        if (!event.persisted) { return; }
        document.querySelectorAll("form[data-loading] button.is-loading").forEach(function (b) {
            b.classList.remove("is-loading");
            b.disabled = false;
        });
    });

})();