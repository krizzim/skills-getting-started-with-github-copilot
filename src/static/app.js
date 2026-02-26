document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      // avoid cached response so we always get latest participants
      const response = await fetch("/activities", { cache: "no-store" });
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // clear previous dropdown options (keep placeholder)
      while (activitySelect.options.length > 1) {
        activitySelect.remove(1);
      }

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        // Build HTML for participants (bulleted list)
        let participantsHTML = "";
        if (details.participants && details.participants.length) {
          const items = details.participants
            .map((email) => `
              <li>
                ${email}
                <span class="remove-participant" data-activity="${name}" data-email="${email}">&times;</span>
              </li>`)
            .join("");
          participantsHTML = `
            <div class="participants">
              <strong>Participants:</strong>
              <ul class="participants-list">
                ${items}
              </ul>
            </div>
          `;
        } else {
          participantsHTML = `
            <div class="participants">
              <strong>Participants:</strong> <span class="none">None yet</span>
            </div>
          `;
        }

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          ${participantsHTML}
        `;

        activitiesList.appendChild(activityCard);

        // attach delete handlers so after building each card we can bind
        activityCard.querySelectorAll(".remove-participant").forEach((el) => {
          el.addEventListener("click", async (evt) => {
            const act = el.dataset.activity;
            const email = el.dataset.email;
            try {
              const res = await fetch(
                `/activities/${encodeURIComponent(act)}/participants?email=${encodeURIComponent(email)}`,
                { method: "DELETE" }
              );
              const json = await res.json();
              if (res.ok) {
                messageDiv.textContent = json.message;
                messageDiv.className = "success";
              } else {
                messageDiv.textContent = json.detail || "Unable to remove participant";
                messageDiv.className = "error";
              }
            } catch (err) {
              console.error("Error removing participant:", err);
              messageDiv.textContent = "Failed to remove participant";
              messageDiv.className = "error";
            }
            messageDiv.classList.remove("hidden");
            setTimeout(() => messageDiv.classList.add("hidden"), 5000);
            fetchActivities();
          });
        });

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        // refresh the list to show the new participant right away
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
