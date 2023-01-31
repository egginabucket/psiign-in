var learners = Array.from(document.getElementsByClassName("learner"));
learners.forEach((l) => {
  l.addEventListener("click", selectName);
});

Array.from(document.getElementsByClassName("action")).forEach((a) => {
  a.addEventListener("click", selectAction);
});

window.setTimeout(() => {
  const lastRecords = document.getElementsByClassName("last-record");
  if (lastRecords.length > 0) {
    const lastRecord = lastRecords[0];
    lastRecord.classList.remove("last-record-visible");
    lastRecord.classList.add("last-record-hidden");
  }
}, 2000);

function getTarget(e) {
  let targ = e.target || e.srcElement;
  if (targ.nodeType == 3)
    // Safari bug
    return targ.parentNode;
  return targ;
}
function selectName(e) {
  document.getElementsByClassName("actions")[0].classList.remove("hidden");
  if (!e) var e = window.event;
  const targ = getTarget(e);
  document.forms[0].elements["learner"].value =
    targ.getAttribute("data-learner-id");
  learners.forEach((l) => {
    l === targ
      ? l.classList.add("learner-selected")
      : l.classList.remove("learner-selected");
  });
}

function selectAction(e) {
  if (!e) var e = window.event;
  e.preventDefault();
  const form = document.forms[0];
  const targ = getTarget(e);
  if (!form.elements["learner"].value) return;
  form.elements["action"].value = targ.getAttribute("data-action-id");
  form.submit();
}
