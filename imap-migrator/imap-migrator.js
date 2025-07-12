// Wraps the entire script in an IIFE to create a private scope and avoid variable conflicts.
(() => {
  // Check if migrator debug is enabled
  const isDebugEnabled =
    typeof translations !== "undefined" &&
    translations.migrator_debug_enabled === true;

  const debugLog = (...args) => {
    if (isDebugEnabled) {
      console.log(...args);
    }
  };

  debugLog("imap-migrator.js: Script started.");

  const init = () => {
    debugLog("imap-migrator.js: init() function called.");

    const logContainer = document.getElementById("log-container");
    const statusIndicator = document.getElementById("status-indicator");

    if (!logContainer) {
      console.error(
        "imap-migrator.js: CRITICAL - Element #log-container not found in DOM."
      );
      return;
    }

    debugLog("imap-migrator.js: Element #log-container found.", logContainer);

    // Update status indicator (always exists now)
    if (statusIndicator) {
      statusIndicator.innerHTML =
        "<i class='fa fa-fw fa-info-circle'></i>&nbsp;<span>Status: " +
        (typeof translations !== "undefined"
          ? translations.status_js_loaded
          : "JavaScript carregado, iniciando monitoramento...") +
        "</span>";
      statusIndicator.className = "alert alert-info";
    }

    // Force initial update with a visible message
    logContainer.innerHTML =
      "<strong>JavaScript is running. Searching for log...</strong>";
    debugLog("imap-migrator.js: Initial content defined.");

    const logFile = logContainer.dataset.logfile;
    let intervalId;
    let lastContent = "";
    let updateCount = 0;

    function forceVisualUpdate(element) {
      // Force multiple visual updates
      element.style.opacity = "0.99";
      element.offsetHeight; // Force reflow
      element.style.opacity = "1";
      element.offsetHeight; // Force reflow again

      // Add a temporary class to force repaint
      element.classList.add("force-update");
      setTimeout(() => {
        element.classList.remove("force-update");
      }, 50);
    }

    function updateLogContent(newContent) {
      debugLog("imap-migrator.js: Updating log content...");
      debugLog("imap-migrator.js: Size of new content:", newContent.length);

      // Convert line breaks to HTML without adding timestamp
      const htmlData = newContent.replace(/\n/g, "<br>");

      // Force DOM update
      logContainer.innerHTML = htmlData;

      // Force scroll to end
      logContainer.scrollTop = logContainer.scrollHeight;

      // Force visual update
      forceVisualUpdate(logContainer);

      debugLog("imap-migrator.js: Log content updated.");
    }

    function updateStatus(message, type = "info") {
      if (statusIndicator) {
        const timestamp = new Date().toLocaleTimeString();
        const alertClass =
          type === "error"
            ? "alert-danger"
            : type === "success"
            ? "alert-success"
            : type === "warning"
            ? "alert-warning"
            : "alert-info";
        const iconClass =
          type === "error"
            ? "fa-exclamation-triangle"
            : type === "success"
            ? "fa-check-circle"
            : type === "warning"
            ? "fa-exclamation-circle"
            : "fa-info-circle";

        statusIndicator.innerHTML = `<i class='fa fa-fw ${iconClass}'></i>&nbsp;<span>Status: [${timestamp}] ${message}</span>`;
        statusIndicator.className = `alert ${alertClass}`;
        forceVisualUpdate(statusIndicator);
      }
    }

    function fetchLog() {
      const currentTime = new Date().toLocaleTimeString();
      debugLog(
        `imap-migrator.js: [${currentTime}] Fetching log at status.cgi?log=${logFile} (attempt ${++updateCount})`
      );

      if (statusIndicator) {
        updateStatus(
          typeof translations !== "undefined"
            ? translations.status_searching_updates + ` (${updateCount})`
            : `Searching for updates... (${updateCount})`,
          "info"
        );
      }

      fetch(`status.cgi?log=${logFile}`, {
        method: "GET",
        cache: "no-cache",
        headers: {
          "Cache-Control": "no-cache",
        },
      })
        .then((response) => {
          debugLog(
            "imap-migrator.js: Response received:",
            response.status,
            response.statusText
          );
          if (!response.ok) {
            console.error(
              "imap-migrator.js: The fetch request failed.",
              response.status,
              response.statusText
            );
            throw new Error(
              `${
                typeof translations !== "undefined"
                  ? translations.error_network_error
                  : "Network error"
              }: ${response.status} ${response.statusText}`
            );
          }
          return response.text();
        })
        .then((data) => {
          debugLog("imap-migrator.js: Data received, size:", data.length);
          debugLog(
            "imap-migrator.js: First 100 characters:",
            data.substring(0, 100)
          );
          debugLog(
            "imap-migrator.js: Last 100 characters:",
            data.substring(data.length - 100)
          );

          // Só atualiza se o conteúdo mudou
          if (data !== lastContent) {
            debugLog("imap-migrator.js: Content changed, updating...");
            updateLogContent(data);
            lastContent = data;
            if (statusIndicator) {
              updateStatus(
                typeof translations !== "undefined"
                  ? translations.status_log_updated
                  : "Log updated successfully",
                "success"
              );
            }
            debugLog("imap-migrator.js: Content updated successfully.");
          } else {
            debugLog("imap-migrator.js: Content unchanged, skipping update.");
            if (statusIndicator) {
              updateStatus(
                typeof translations !== "undefined"
                  ? translations.status_waiting_updates
                  : "Waiting for new updates...",
                "warning"
              );
            }
          }

          if (data.includes("Exiting with return value")) {
            debugLog(
              "imap-migrator.js: End of migration detected. Stopping search."
            );
            clearInterval(intervalId);
            if (statusIndicator) {
              updateStatus(
                typeof translations !== "undefined"
                  ? translations.status_migration_complete
                  : "Migration complete!",
                "success"
              );
            }
            const completeMessage = document.createElement("b");
            completeMessage.textContent =
              typeof translations !== "undefined"
                ? translations.migration_complete
                : "Migration Complete.";
            logContainer.appendChild(document.createElement("br"));
            logContainer.appendChild(completeMessage);
          }
        })
        .catch((error) => {
          console.error(
            "imap-migrator.js: Error during search (fetch):",
            error
          );
          if (statusIndicator) {
            updateStatus(
              typeof translations !== "undefined"
                ? translations.status_error_search
                : "Error searching for updates",
              "error"
            );
          }
          logContainer.innerHTML =
            "<strong>" +
            (typeof translations !== "undefined"
              ? translations.error_js_error
              : "JAVASCRIPT ERROR") +
            ": " +
            error.message +
            ". Check console.</strong>";
          clearInterval(intervalId);
        });
    }

    if (logFile) {
      debugLog("imap-migrator.js: Log file name found. Starting search.");
      if (statusIndicator) {
        updateStatus(
          typeof translations !== "undefined"
            ? "Iniciando monitoramento do log..."
            : "Starting log monitoring...",
          "info"
        );
      }
      intervalId = setInterval(fetchLog, 2000); // Busca a cada 2 segundos
      fetchLog(); // Primeira busca imediata
    } else {
      console.error(
        "imap-migrator.js: CRITICAL - data-logfile attribute not found."
      );
      if (statusIndicator) {
        updateStatus(
          typeof translations !== "undefined"
            ? translations.status_error_log_file
            : "Error: Log file not found",
          "error"
        );
      }
      logContainer.innerHTML =
        "<strong>" +
        (typeof translations !== "undefined"
          ? translations.error_log_file_not_found
          : "ERROR: Could not find log file name.") +
        "</strong>";
    }
  };

  // Robust approach to ensure DOM is ready.
  if (document.readyState === "loading") {
    debugLog("imap-migrator.js: DOM loading. Adding listener.");
    document.addEventListener("DOMContentLoaded", init);
  } else {
    debugLog(
      "imap-migrator.js: DOM is already ready. Calling init() directly."
    );
    init();
  }
})();
