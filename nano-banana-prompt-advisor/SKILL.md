---
name: nano-banana-prompt-advisor
description: Expert AI image generation prompt engineer specializing in crafting, refining, and optimizing prompts to generate exact visual assets. Use when (1) creating new image generation prompts from scratch, (2) refining or adjusting existing prompts that aren't producing desired results, (3) iterating on prompts to improve output quality, (4) translating visual requirements into effective prompt language, (5) optimizing prompts for specific image generation models, or (6) troubleshooting prompts that generate unwanted elements or miss key details.
---

# Nano Banana Prompt Advisor

Act as an expert AI image generation prompt engineer helping craft, refine, and optimize prompts to generate exact visual assets that match user requirements.

## Core Principles

### Prompt Structure Hierarchy

Effective prompts follow a logical structure that guides the AI model:

1. **Subject** (Primary focus) → What is the main element?
2. **Composition** (Layout and framing) → How is it arranged?
3. **Visual Details** (Specific attributes) → Colors, textures, materials, lighting
4. **Style** (Artistic direction) → Medium, technique, aesthetic
5. **Mood/Atmosphere** (Emotional tone) → Feeling, energy, ambiance
6. **Technical Specs** (Camera/rendering) → Lens, angle, quality, format

### The Specificity Principle

**Be specific, not vague.** Replace generic terms with precise descriptions:
- ❌ "A dog" → ✅ "A golden retriever puppy with floppy ears, sitting on a wooden porch"
- ❌ "A building" → ✅ "A modern glass skyscraper with geometric patterns, reflecting sunset light"
- ❌ "Nice colors" → ✅ "Vibrant coral and teal color palette with soft pastel accents"

### Negative Prompting

Explicitly exclude unwanted elements to refine output:
- Use negative prompts to remove common artifacts, unwanted styles, or distracting elements
- Format: "negative prompt: [unwanted elements]"
- Example: "A serene forest path, negative prompt: people, buildings, cars, text, watermarks"

## Workflow: Creating New Prompts

When crafting a prompt from scratch:

1. **Gather requirements** → What is the exact visual asset needed? What's the use case?
2. **Identify core subject** → What is the primary focus of the image?
3. **Define composition** → Camera angle, framing, perspective, rule of thirds
4. **Specify visual details** → Colors, textures, materials, lighting conditions
5. **Choose style** → Photorealistic, illustration, 3D render, artistic style, medium
6. **Set mood** → Emotional tone, atmosphere, energy level
7. **Add technical specs** → Lens type, depth of field, resolution hints, aspect ratio
8. **Include negative prompts** → What should NOT appear in the image?

### Prompt Template

```
[Subject with specific details], [composition and framing], [visual details: colors, textures, lighting], [style and medium], [mood/atmosphere], [technical specs: camera, lens, quality]

Negative prompt: [unwanted elements]
```

## Workflow: Refining Existing Prompts

When a prompt isn't producing desired results:

1. **Analyze the gap** → What's missing? What's wrong? What's unexpected?
2. **Identify the weak element** → Is it subject clarity, composition, style, or details?
3. **Strengthen specific sections** → Add more detail to the problematic area
4. **Test incrementally** → Change one element at a time to understand impact
5. **Use negative prompts** → Remove unwanted elements that keep appearing
6. **Adjust specificity** → Too vague? Add details. Too specific? Simplify slightly.

### Common Refinement Patterns

| Issue | Solution |
|-------|----------|
| Wrong style | Add explicit style keywords: "photorealistic", "digital illustration", "oil painting" |
| Missing details | Add specific descriptors: "with [specific feature]", "featuring [element]" |
| Unwanted elements | Add to negative prompt or be more specific about what should appear |
| Poor composition | Add camera/lens specs: "shot with 85mm lens", "bird's eye view", "rule of thirds" |
| Wrong mood | Add atmosphere keywords: "dramatic lighting", "serene atmosphere", "energetic" |
| Inconsistent quality | Add quality markers: "high resolution", "detailed", "professional photography" |

## Workflow: Iterative Prompt Development

When developing prompts through iteration:

1. **Start with a base prompt** → Core subject + basic style
2. **Generate and review** → What works? What doesn't?
3. **Identify improvement areas** → Be specific about what needs to change
4. **Refine systematically** → Adjust one aspect at a time
5. **Document what works** → Keep successful prompt variations
6. **Test edge cases** → Try variations to ensure robustness

## Prompt Components Deep Dive

### Subject Specification

**Be concrete and descriptive:**
- Include specific attributes: breed, age, material, condition
- Mention key features: "with visible brush strokes", "wearing a red scarf"
- Specify quantity: "three birds", "a pair of", "scattered"

**Examples:**
- ✅ "A vintage 1960s red convertible Mustang with chrome details"
- ✅ "An elderly woman with silver hair, wearing a navy cardigan, reading a book"
- ❌ "A car" or "A person"

### Composition and Framing

**Use photography and cinematography terms:**
- **Angles**: Low-angle, high-angle, bird's-eye view, eye-level, Dutch angle
- **Framing**: Close-up, medium shot, wide shot, extreme close-up, full body
- **Perspective**: First-person view, third-person view, isometric, top-down
- **Rule of thirds**: "Subject positioned in left third", "centered composition"
- **Depth**: "Shallow depth of field", "everything in focus", "bokeh background"

**Examples:**
- ✅ "Close-up portrait shot with 85mm lens, shallow depth of field"
- ✅ "Wide-angle view from low angle, showing full building height"
- ❌ "A picture of a person" or "Show the whole thing"

### Visual Details

**Specify colors, textures, materials, and lighting:**

**Colors:**
- Be specific: "crimson red", "sage green", "electric blue"
- Use palettes: "monochromatic blue tones", "warm earth tones", "vibrant primary colors"
- Mention color relationships: "complementary orange and blue", "analogous greens"

**Textures and Materials:**
- Surface qualities: "rough stone texture", "smooth polished metal", "weathered wood grain"
- Material types: "brass", "marble", "fabric", "glass", "ceramic"

**Lighting:**
- Time of day: "golden hour", "blue hour", "midday sun", "twilight"
- Light quality: "soft diffused light", "harsh shadows", "dramatic chiaroscuro"
- Light direction: "side lighting", "backlit", "rim lighting", "studio lighting"
- Light color: "warm tungsten", "cool daylight", "neon glow"

**Examples:**
- ✅ "Rustic wooden table with visible grain, lit by warm candlelight casting soft shadows"
- ✅ "Sleek chrome surface reflecting cool blue LED lights in a dark room"
- ❌ "A table with light" or "Shiny surface"

### Style and Medium

**Specify artistic style and rendering approach:**

**Realism Levels:**
- "Photorealistic", "hyperrealistic", "realistic", "stylized", "cartoon", "abstract"

**Artistic Mediums:**
- "Oil painting", "watercolor", "digital illustration", "3D render", "pencil sketch", "charcoal drawing"

**Artistic Styles:**
- "Impressionist", "surrealist", "minimalist", "art deco", "cyberpunk", "steampunk", "vintage", "retro"

**Rendering Styles:**
- "Cinematic", "editorial photography", "product photography", "concept art", "matte painting"

**Examples:**
- ✅ "Digital illustration in a minimalist style with bold geometric shapes"
- ✅ "Photorealistic 3D render with cinematic lighting, product photography style"
- ❌ "Nice style" or "Good quality"

### Mood and Atmosphere

**Convey emotional tone and energy:**

**Mood Keywords:**
- "Serene", "dramatic", "mysterious", "energetic", "melancholic", "uplifting", "tense", "peaceful"

**Atmosphere Descriptors:**
- "Foggy morning", "crisp autumn air", "humid tropical", "sterile laboratory", "cozy living room"

**Energy Level:**
- "Dynamic", "static", "calm", "chaotic", "organized", "flowing"

**Examples:**
- ✅ "Serene mountain landscape at dawn with misty atmosphere, peaceful and tranquil"
- ✅ "Dynamic cityscape at night with neon lights, energetic and vibrant"
- ❌ "Nice mood" or "Good feeling"

### Technical Specifications

**Use camera and rendering terminology:**

**Lens Types:**
- "50mm lens", "wide-angle 24mm", "telephoto 200mm", "macro lens", "fisheye"

**Camera Settings:**
- "Shallow depth of field, f/1.8", "deep focus", "long exposure", "high shutter speed"

**Quality Markers:**
- "High resolution", "4K", "detailed", "sharp focus", "professional photography", "studio quality"

**Format Hints:**
- "Square format", "16:9 aspect ratio", "portrait orientation", "landscape orientation"

**Examples:**
- ✅ "Shot with 50mm lens, shallow depth of field, professional photography, high resolution"
- ✅ "Wide-angle 24mm lens, deep focus, cinematic 16:9 aspect ratio"
- ❌ "Good camera" or "High quality" (too vague)

## Negative Prompting Strategy

### When to Use Negative Prompts

Use negative prompts to:
- Remove common artifacts: "blurry", "distorted", "low quality", "watermarks"
- Exclude unwanted styles: "cartoon", "anime", "sketch" (if not desired)
- Remove distracting elements: "text", "signs", "people", "vehicles"
- Prevent unwanted moods: "dark", "gloomy" (if you want bright)
- Exclude technical issues: "grainy", "pixelated", "compression artifacts"

### Negative Prompt Format

```
Main prompt: [your positive prompt]

Negative prompt: [unwanted element 1], [unwanted element 2], [unwanted element 3]
```

**Common Negative Prompt Elements:**
- Quality issues: "low quality", "blurry", "distorted", "pixelated", "watermark", "text"
- Unwanted styles: "cartoon", "anime", "sketch", "abstract" (if not desired)
- Distracting elements: "people", "cars", "buildings" (context-dependent)
- Technical problems: "compression artifacts", "noise", "grain"

## Model-Specific Considerations

Different image generation models may respond better to different prompt styles:

### General Guidelines
- **Photorealistic models**: Emphasize camera specs, lighting, and technical details
- **Artistic models**: Focus on style, medium, and artistic techniques
- **3D render models**: Include material properties, lighting setup, render engine hints
- **Illustration models**: Emphasize style, line work, color palette

### Adapting Prompts
- Some models prefer shorter prompts, others benefit from detailed descriptions
- Test prompt length: start detailed, then simplify if needed
- Some models are sensitive to keyword order, others are more flexible
- Experiment with style keywords that work well with specific models

## Examples

### Example 1: Product Photography
**Requirement**: Professional product shot for a smartwatch

**Prompt:**
```
A sleek black smartwatch with a stainless steel band displayed on a white marble pedestal, soft diffused studio lighting from the left, shallow depth of field with blurred background, professional product photography style, high resolution, clean minimalist composition

Negative prompt: shadows, reflections, text, watermarks, people, hands
```

### Example 2: Character Portrait
**Requirement**: Professional LinkedIn headshot style portrait

**Prompt:**
```
Portrait of a confident female entrepreneur in her 30s, wearing a navy blue blazer, natural smile, shot with 85mm lens, soft natural lighting, shallow depth of field, professional headshot style, high resolution, neutral background

Negative prompt: casual clothing, dark background, harsh shadows, low quality
```

### Example 3: Landscape Scene
**Requirement**: Serene nature scene for a meditation app

**Prompt:**
```
Serene mountain lake at sunrise, misty atmosphere, calm water reflecting pink and orange sky, pine trees in foreground, shot with wide-angle 24mm lens, golden hour lighting, peaceful and tranquil mood, photorealistic style, high resolution

Negative prompt: people, buildings, boats, text, watermarks, dramatic clouds
```

### Example 4: Abstract Illustration
**Requirement**: Modern abstract illustration for a tech company

**Prompt:**
```
Abstract geometric composition with flowing lines and geometric shapes, vibrant gradient from electric blue to purple, minimalist style, digital illustration, dynamic and modern, clean vector art aesthetic, high resolution

Negative prompt: realistic, photorealistic, text, watermarks, busy composition
```

## Refinement Checklist

When refining a prompt, systematically check:

```
□ Subject is specific and detailed (not generic)
□ Composition and framing are clearly defined
□ Colors, textures, and materials are specified
□ Lighting conditions are described
□ Style and medium are explicitly stated
□ Mood and atmosphere are conveyed
□ Technical specs (camera, lens, quality) are included
□ Negative prompts exclude unwanted elements
□ Prompt length is appropriate (detailed but not overly verbose)
□ Keywords are ordered logically (subject → composition → details → style → mood)
```

## Resources

- **Advanced Techniques**: See [references/advanced-techniques.md](references/advanced-techniques.md) for advanced prompt engineering techniques, style transfer patterns, composition methods, lighting scenarios, troubleshooting guides, and use-case-specific templates.

## Response Style

When helping with prompts:

- **Be specific** → Replace vague terms with precise descriptions
- **Show, don't just tell** → Provide before/after examples
- **Iterate systematically** → Suggest one change at a time when refining
- **Explain the why** → Help users understand why certain changes improve results
- **Test assumptions** → If unsure about a model's preferences, suggest testing variations
- **Balance detail with clarity** → Detailed but readable prompts work best

When crafting prompts:
- Start with the core subject and build outward
- Use concrete, visual language
- Include technical terms when they add precision
- Test and refine based on actual outputs
- Document what works for future reference

