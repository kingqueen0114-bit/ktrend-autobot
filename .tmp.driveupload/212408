import { Schema } from "@sanity/schema";
import { builtinTypes } from "@sanity/schema/_internal";
import { defineType, defineField } from "@sanity/types";
function createPortableTextMemberSchemaTypes(portableTextType) {
  if (!portableTextType)
    throw new Error("Parameter 'portabletextType' missing (required)");
  const blockType = portableTextType.of?.find(findBlockType);
  if (!blockType)
    throw new Error("Block type is not defined in this schema (required)");
  const childrenField = blockType.fields?.find(
    (field) => field.name === "children"
  );
  if (!childrenField)
    throw new Error("Children field for block type found in schema (required)");
  const ofType = childrenField.type.of;
  if (!ofType)
    throw new Error(
      "Valid types for block children not found in schema (required)"
    );
  const spanType = ofType.find((memberType) => memberType.name === "span");
  if (!spanType)
    throw new Error("Span type not found in schema (required)");
  const inlineObjectTypes = ofType.filter(
    (memberType) => memberType.name !== "span"
  ) || [], blockObjectTypes = portableTextType.of?.filter(
    (field) => field.name !== blockType.name
  ) || [];
  return {
    styles: resolveEnabledStyles(blockType),
    decorators: resolveEnabledDecorators(spanType),
    lists: resolveEnabledListItems(blockType),
    block: blockType,
    span: spanType,
    portableText: portableTextType,
    inlineObjects: inlineObjectTypes,
    blockObjects: blockObjectTypes,
    annotations: spanType.annotations
  };
}
function resolveEnabledStyles(blockType) {
  const styleField = blockType.fields?.find(
    (btField) => btField.name === "style"
  );
  if (!styleField)
    throw new Error(
      "A field with name 'style' is not defined in the block type (required)."
    );
  const textStyles = styleField.type.options?.list && styleField.type.options.list?.filter(
    (style) => style.value
  );
  if (!textStyles || textStyles.length === 0)
    throw new Error(
      "The style fields need at least one style defined. I.e: {title: 'Normal', value: 'normal'}."
    );
  return textStyles;
}
function resolveEnabledDecorators(spanType) {
  return spanType.decorators;
}
function resolveEnabledListItems(blockType) {
  const listField = blockType.fields?.find(
    (btField) => btField.name === "listItem"
  );
  if (!listField)
    throw new Error(
      "A field with name 'listItem' is not defined in the block type (required)."
    );
  const listItems = listField.type.options?.list && listField.type.options.list.filter((list) => list.value);
  if (!listItems)
    throw new Error("The list field need at least to be an empty array");
  return listItems;
}
function findBlockType(type) {
  return type.type ? findBlockType(type.type) : type.name === "block" ? type : null;
}
function portableTextMemberSchemaTypesToSchema(schema) {
  return {
    annotations: schema.annotations.map((annotation) => ({
      name: annotation.name,
      fields: annotation.fields.map((field) => ({
        name: field.name,
        type: field.type.jsonType,
        title: field.type.title
      })),
      title: annotation.title
    })),
    block: {
      name: schema.block.name
    },
    blockObjects: schema.blockObjects.map((blockObject) => ({
      name: blockObject.name,
      fields: blockObject.fields.map((field) => ({
        name: field.name,
        type: field.type.jsonType,
        title: field.type.title
      })),
      title: blockObject.title
    })),
    decorators: schema.decorators.map((decorator) => ({
      name: decorator.value,
      title: decorator.title,
      value: decorator.value
    })),
    inlineObjects: schema.inlineObjects.map((inlineObject) => ({
      name: inlineObject.name,
      fields: inlineObject.fields.map((field) => ({
        name: field.name,
        type: field.type.jsonType,
        title: field.type.title
      })),
      title: inlineObject.title
    })),
    span: {
      name: schema.span.name
    },
    styles: schema.styles.map((style) => ({
      name: style.value,
      title: style.title,
      value: style.value
    })),
    lists: schema.lists.map((list) => ({
      name: list.value,
      title: list.title,
      value: list.value
    }))
  };
}
function sanitySchemaToPortableTextSchema(sanitySchema) {
  const portableTextMemberSchemaTypes = createPortableTextMemberSchemaTypes(
    sanitySchema.hasOwnProperty("jsonType") ? sanitySchema : compileType(sanitySchema)
  );
  return portableTextMemberSchemaTypesToSchema(portableTextMemberSchemaTypes);
}
function compileType(rawType) {
  return Schema.compile({
    name: "blockTypeSchema",
    types: [rawType, ...builtinTypes]
  }).get(rawType.name);
}
const keyGenerator = () => randomKey(12), getByteHexTable = /* @__PURE__ */ (() => {
  let table;
  return () => {
    if (table)
      return table;
    table = [];
    for (let i = 0; i < 256; ++i)
      table[i] = (i + 256).toString(16).slice(1);
    return table;
  };
})();
function whatwgRNG(length = 16) {
  const rnds8 = new Uint8Array(length);
  return crypto.getRandomValues(rnds8), rnds8;
}
function randomKey(length) {
  const table = getByteHexTable();
  return whatwgRNG(length).reduce((str, n) => str + table[n], "").slice(0, length);
}
function startCase(str) {
  return str.replace(/([a-z])([A-Z])/g, "$1 $2").replace(/[_-]+/g, " ").trim().split(/\s+/).filter(Boolean).map((word) => word.charAt(0).toUpperCase() + word.slice(1)).join(" ");
}
const defaultObjectTitles = {
  image: "Image",
  url: "URL"
}, sanityBuiltinNames = /* @__PURE__ */ new Set(["file", "geopoint", "image", "slug", "url"]);
function compileSchemaDefinitionToPortableTextMemberSchemaTypes(definition) {
  const blockObjectDefs = definition?.blockObjects ?? [], inlineObjectDefs = definition?.inlineObjects ?? [], blockObjectNameSet = new Set(
    blockObjectDefs.map((blockObject) => blockObject.name)
  ), inlineObjectNameSet = new Set(
    inlineObjectDefs.map((inlineObject) => inlineObject.name)
  ), temporaryBlockObjectNames = {}, temporaryInlineObjectNames = {}, blockObjectNames = {}, inlineObjectNames = {};
  for (const name of blockObjectNameSet)
    if (sanityBuiltinNames.has(name) || inlineObjectNameSet.has(name)) {
      const tmpName = `tmp-${keyGenerator()}-${name}`;
      temporaryBlockObjectNames[name] = tmpName, blockObjectNames[tmpName] = name;
    }
  for (const name of inlineObjectNameSet)
    if (sanityBuiltinNames.has(name) || blockObjectNameSet.has(name)) {
      const tmpName = `tmp-${keyGenerator()}-${name}`;
      temporaryInlineObjectNames[name] = tmpName, inlineObjectNames[tmpName] = name;
    }
  const blockObjects = blockObjectDefs.map(
    (blockObject) => defineType({
      type: "object",
      // Use temporary names to work around `SanitySchema.compile` adding
      // default fields to objects with certain names, and to avoid duplicate
      // type names when a type appears in both blockObjects and inlineObjects.
      name: temporaryBlockObjectNames[blockObject.name] ?? blockObject.name,
      title: blockObject.title === void 0 ? (
        // This avoids the default title which is a title case of the object name
        defaultObjectTitles[blockObject.name]
      ) : blockObject.title,
      fields: blockObject.fields?.map((field) => ({
        name: field.name,
        type: field.type,
        title: field.title ?? startCase(field.name)
      })) ?? []
    })
  ), inlineObjects = inlineObjectDefs.map(
    (inlineObject) => defineType({
      type: "object",
      // Use temporary names to work around `SanitySchema.compile` adding
      // default fields to objects with certain names, and to avoid duplicate
      // type names when a type appears in both blockObjects and inlineObjects.
      name: temporaryInlineObjectNames[inlineObject.name] ?? inlineObject.name,
      title: inlineObject.title === void 0 ? (
        // This avoids the default title which is a title case of the object name
        defaultObjectTitles[inlineObject.name]
      ) : inlineObject.title,
      fields: inlineObject.fields?.map((field) => ({
        name: field.name,
        type: field.type,
        title: field.title ?? startCase(field.name)
      })) ?? []
    })
  ), portableTextSchema = defineField({
    type: "array",
    name: "portable-text",
    of: [
      ...blockObjects.map((blockObject) => ({ type: blockObject.name })),
      {
        type: "block",
        name: "block",
        of: inlineObjects.map((inlineObject) => ({ type: inlineObject.name })),
        marks: {
          decorators: definition?.decorators?.map((decorator) => ({
            title: decorator.title ?? startCase(decorator.name),
            value: decorator.name
          })) ?? [],
          annotations: definition?.annotations?.map((annotation) => ({
            name: annotation.name,
            type: "object",
            title: annotation.title,
            fields: annotation.fields?.map((field) => ({
              name: field.name,
              title: field.title ?? startCase(field.name),
              type: field.type
            })) ?? []
          })) ?? []
        },
        lists: definition?.lists?.map((list) => ({
          value: list.name,
          title: list.title ?? startCase(list.name)
        })) ?? [],
        styles: definition?.styles?.map((style) => ({
          value: style.name,
          title: style.title ?? startCase(style.name)
        })) ?? []
      }
    ]
  }), schema = Schema.compile({
    types: [portableTextSchema, ...blockObjects, ...inlineObjects]
  }).get("portable-text"), pteSchema = createPortableTextMemberSchemaTypes(schema);
  for (const blockObject of pteSchema.blockObjects) {
    const originalName = blockObjectNames[blockObject.name];
    originalName !== void 0 && (blockObject.name = originalName, blockObject.type && (blockObject.type = { ...blockObject.type, name: originalName }));
  }
  for (const inlineObject of pteSchema.inlineObjects) {
    const originalName = inlineObjectNames[inlineObject.name];
    originalName !== void 0 && (inlineObject.name = originalName, inlineObject.type && (inlineObject.type = { ...inlineObject.type, name: originalName }));
  }
  return pteSchema;
}
export {
  compileSchemaDefinitionToPortableTextMemberSchemaTypes,
  createPortableTextMemberSchemaTypes,
  portableTextMemberSchemaTypesToSchema,
  sanitySchemaToPortableTextSchema
};
//# sourceMappingURL=index.js.map
