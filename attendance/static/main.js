var learners = Array.from(document.getElementsByClassName("learner"));
learners.forEach((l) => {
  l.addEventListener("click", selectName);
});

Array.from(document.getElementsByClassName("action")).forEach((l) => {
  l.addEventListener("click", selectAction);
});

function getTarget(e) {
  let targ = e.target || e.srcElement;
  if (targ.nodeType == 3)
    // Safari bug
    targ = targ.parentNode;
  return targ;
}
function selectName(e) {
  document.getElementsByClassName("actions")[0].classList.remove("hidden");
  if (!e) var e = window.event;
  const targ = getTarget(e);
  document.forms[0].elements["learner"].value = targ.getAttribute("learner-id");
  learners.forEach((l) => {
    l === targ
      ? l.classList.add("learner-selected")
      : l.classList.remove("learner-selected");
  });
}

function selectAction(e) {
  if (!e) var e = window.event;
  e.preventDefault();
  const form = document.forms[0]
  const targ = getTarget(e);
  if (!form.elements["learner"].value)
    return
  form.elements["action"].value = targ.getAttribute("action-id");
  form.submit();
}
