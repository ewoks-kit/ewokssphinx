// Tag filter for Ewoks task sections. Clicking a tag cycles it through
// "include" -> "exclude" -> neutral. A task is shown when it has at least one
// included tag (if any) and no excluded tag. The state is kept in the URL query
// (`include_tags` and `exclude_tags`) so it survives navigation and can be shared.
// Each group of sibling task sections with tags gets its own filter bar, so a bar
// is always next to the tasks it filters. All bars share the same state. Groups
// without tags are not filtered.
(function () {
  "use strict";

  const STATES = ["", "include", "exclude"];

  function taskTags(section) {
    return Array.from(section.querySelectorAll(".ewokssphinx-tags .ewokssphinx-tag")).map(
      (el) => el.textContent.trim()
    );
  }

  function readState() {
    const params = new URLSearchParams(window.location.search);
    const state = new Map();
    for (const key of ["include", "exclude"]) {
      const value = params.get(key + "_tags");
      if (!value) continue;
      for (const tag of value.split(",")) {
        if (tag) state.set(tag, key);
      }
    }
    return state;
  }

  function writeState(state) {
    const url = new URL(window.location.href);
    for (const key of ["include", "exclude"]) {
      const tags = Array.from(state.entries())
        .filter(([, value]) => value === key)
        .map(([tag]) => tag);
      if (tags.length) url.searchParams.set(key + "_tags", tags.join(","));
      else url.searchParams.delete(key + "_tags");
    }
    window.history.replaceState(null, "", url);
  }

  function init() {
    // Group task sections by parent and keep the groups with tags
    const groups = new Map();
    for (const section of document.querySelectorAll("section.ewokssphinx-task")) {
      if (!groups.has(section.parentNode)) groups.set(section.parentNode, []);
      groups.get(section.parentNode).push(section);
    }
    const taggedGroups = Array.from(groups.values())
      .map((groupSections) => ({
        sections: groupSections,
        tags: new Map(groupSections.map((s) => [s, taskTags(s)])),
      }))
      .filter((group) => Array.from(group.tags.values()).some((tags) => tags.length));
    if (!taggedGroups.length) return;

    const sections = taggedGroups.flatMap((group) => group.sections);
    const sectionTags = new Map(taggedGroups.flatMap((group) => Array.from(group.tags)));

    // Model sections and the task sections using them
    const modelTasks = new Map(
      Array.from(document.querySelectorAll("section.ewokssphinx-model"))
        .map((m) => {
          const cls = Array.from(m.classList).find((c) => c.startsWith("ewokssphinx-model-"));
          return [m, cls ? sections.filter((s) => s.classList.contains(cls)) : []];
        })
        .filter(([, tasks]) => tasks.length)
    );
    const modelSections = Array.from(modelTasks.keys());
    const modelsSections = Array.from(
      new Set(modelSections.map((m) => m.closest("section.ewokssphinx-models")).filter(Boolean))
    );

    // Table-of-contents entries pointing to task and model sections
    const tocLinks = new Map(
      [...sections, ...modelSections, ...modelsSections].map((s) => [
        s,
        s.id
          ? Array.from(document.querySelectorAll(`a[href="#${CSS.escape(s.id)}"]`))
              .filter((a) => !s.contains(a))
              .map((a) => a.closest("li") || a)
          : [],
      ])
    );

    function setVisible(section, show) {
      section.style.display = show ? "" : "none";
      for (const link of tocLinks.get(section)) link.style.display = show ? "" : "none";
    }

    const state = readState();

    for (const group of taggedGroups) {
      const groupTags = Array.from(new Set(Array.from(group.tags.values()).flat())).sort();
      const bar = document.createElement("div");
      bar.className = "ewokssphinx-tag-filter";
      const label = document.createElement("span");
      label.textContent = "Filter on tags:";
      bar.appendChild(label);
      for (const tag of groupTags) {
        const chip = document.createElement("code");
        chip.className = "ewokssphinx-tag";
        chip.textContent = tag;
        bar.appendChild(chip);
      }
      group.count = document.createElement("span");
      group.count.className = "ewokssphinx-tag-filter-count";
      bar.appendChild(group.count);
      group.sections[0].parentNode.insertBefore(bar, group.sections[0]);
    }

    function apply() {
      const include = new Set();
      const exclude = new Set();
      for (const [tag, value] of state) {
        if (value === "include") include.add(tag);
        else if (value === "exclude") exclude.add(tag);
      }
      for (const [section, tags] of sectionTags) {
        const show =
          (!include.size || tags.some((t) => include.has(t))) &&
          !tags.some((t) => exclude.has(t));
        setVisible(section, show);
      }
      for (const [model, tasks] of modelTasks) {
        setVisible(model, tasks.some((t) => t.style.display !== "none"));
      }
      for (const models of modelsSections) {
        const children = Array.from(models.querySelectorAll(":scope > section.ewokssphinx-model"));
        setVisible(models, children.some((m) => m.style.display !== "none"));
      }
      for (const chip of document.querySelectorAll(".ewokssphinx-tag")) {
        const value = state.get(chip.textContent.trim()) || "";
        chip.classList.toggle("ewokssphinx-tag-include", value === "include");
        chip.classList.toggle("ewokssphinx-tag-exclude", value === "exclude");
      }
      for (const group of taggedGroups) {
        const visible = group.sections.filter((s) => s.style.display !== "none").length;
        group.count.textContent =
          include.size || exclude.size ? `${visible} of ${group.sections.length} tasks` : "";
      }
    }

    document.addEventListener("click", (event) => {
      const chip = event.target.closest(".ewokssphinx-tag");
      if (!chip) return;
      const tag = chip.textContent.trim();
      const next = STATES[(STATES.indexOf(state.get(tag) || "") + 1) % STATES.length];
      if (next) state.set(tag, next);
      else state.delete(tag);
      writeState(state);
      apply();
    });

    apply();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
