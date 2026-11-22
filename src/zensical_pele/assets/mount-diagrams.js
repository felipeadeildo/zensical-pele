// Mounts the diagrams of the current page with Pele. Instant navigation runs
// this module again on every page, so mounted diagrams are tracked globally and
// released once their page is gone.

const peleUrl = __PELE_URL__;
const diagramSelector = __DIAGRAM_SELECTOR__;
const mountOptions = __MOUNT_OPTIONS__;

const registry = (globalThis.__zensicalPele ??= { mounted: [] });

registry.mounted = registry.mounted.filter(({ element, diagram }) => {
  if (element.isConnected) return true;
  diagram.destroy?.();
  return false;
});

const elements = [...document.querySelectorAll(diagramSelector)].filter(
  (element) => !element.dataset.peleState,
);

if (elements.length > 0) {
  for (const element of elements) element.dataset.peleState = "loading";

  const pele = await import(peleUrl);
  const mount = pele.mountAsync ?? pele.mount;

  await Promise.all(elements.map((element) => mountDiagram(element, mount)));
}

async function mountDiagram(element, mount) {
  const source = element.textContent ?? "";
  try {
    element.textContent = "";
    const diagram = await mount(element, source, {
      onError: (error) => console.warn("[zensical-pele]", error),
      ...mountOptions,
    });
    element.dataset.peleState = "mounted";
    registry.mounted.push({ element, diagram });
  } catch (error) {
    element.textContent = source;
    element.dataset.peleState = "failed";
    console.error("[zensical-pele]", error);
  }
}
