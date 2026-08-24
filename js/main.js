/* Loroz Custom Boats — site interactions */
(function () {
  "use strict";

  /* Mobile nav toggle */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        nav.classList.remove("open");
        toggle.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* Sticky header shadow on scroll */
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      header.style.boxShadow = window.scrollY > 8 ? "0 4px 18px rgba(0,0,0,0.25)" : "none";
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* Forms: validate, show success, offer email fallback */
  var forms = document.querySelectorAll("form[data-form]");
  Array.prototype.forEach.call(forms, function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true;
      var fields = form.querySelectorAll("[required]");
      Array.prototype.forEach.call(fields, function (f) {
        if (!f.value.trim()) {
          ok = false;
          f.style.borderColor = "#e64a20";
        } else {
          f.style.borderColor = "";
        }
      });
      if (!ok) return;

      /* Build a mailto fallback so leads still reach the shop without a backend */
      var data = {};
      Array.prototype.forEach.call(form.querySelectorAll("[name]"), function (f) {
        if (f.value.trim()) data[f.name] = f.value.trim();
      });
      var subject = encodeURIComponent((data.serviceType ? data.serviceType + " - " : "") + "Website Inquiry - LorozBoats.com");
      var bodyLines = [];
      Object.keys(data).forEach(function (k) {
        bodyLines.push(k + ": " + data[k]);
      });
      var body = encodeURIComponent(bodyLines.join("\n"));

      var mailto = document.createElement("a");
      mailto.href = "mailto:info@lorozboats.com?subject=" + subject + "&body=" + body;
      mailto.style.display = "none";
      document.body.appendChild(mailto);
      mailto.click();
      document.body.removeChild(mailto);

      var success = form.querySelector(".form-success");
      if (success) {
        success.classList.add("show");
        success.innerHTML = "Thanks! Your request is ready to send from your email app. Prefer to talk now? Call <strong>941-313-2191</strong>.";
      }
      form.reset();
    });
  });

  /* Light reveal on scroll */
  var reveals = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            en.target.style.opacity = "1";
            en.target.style.transform = "none";
            io.unobserve(en.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    Array.prototype.forEach.call(reveals, function (el) {
      el.style.opacity = "0";
      el.style.transform = "translateY(14px)";
      el.style.transition = "opacity 0.5s ease, transform 0.5s ease";
      io.observe(el);
    });
  }

  /* Current year in footer */
  var yr = document.querySelector("[data-year]");
  if (yr) yr.textContent = new Date().getFullYear();
})();
