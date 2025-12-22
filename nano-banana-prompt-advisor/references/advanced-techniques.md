# Advanced Prompt Engineering Techniques

## Table of Contents

1. [Prompt Weighting and Emphasis](#prompt-weighting-and-emphasis)
2. [Style Transfer Patterns](#style-transfer-patterns)
3. [Composition Techniques](#composition-techniques)
4. [Lighting Scenarios](#lighting-scenarios)
5. [Color Theory Application](#color-theory-application)
6. [Troubleshooting Common Issues](#troubleshooting-common-issues)
7. [Prompt Templates by Use Case](#prompt-templates-by-use-case)

## Prompt Weighting and Emphasis

Some models support emphasis through syntax like `(keyword)` for normal weight, `((keyword))` for increased emphasis, or `[keyword]` for decreased emphasis.

**Examples:**
- `A ((vibrant)) sunset` - Emphasizes vibrant
- `A [subtle] sunset` - De-emphasizes subtle
- `((dramatic lighting))` - Strong emphasis on lighting

**When to use:**
- Emphasize critical elements that keep getting missed
- De-emphasize elements that are too prominent
- Balance competing priorities in a prompt

## Style Transfer Patterns

Combine multiple style references for unique results:

**Pattern 1: Style + Medium**
- "Digital illustration in the style of [artist name]"
- "Oil painting with impressionist techniques"
- "3D render with photorealistic materials"

**Pattern 2: Era + Style**
- "1950s retro-futuristic design"
- "Medieval fantasy with modern digital art style"
- "Victorian steampunk aesthetic"

**Pattern 3: Cultural + Technical**
- "Japanese minimalist design with Scandinavian color palette"
- "Art Deco architecture with cyberpunk lighting"

## Composition Techniques

### Rule of Thirds Application
- "Subject positioned in the left third of the frame"
- "Horizon line at the lower third"
- "Key element at the intersection of thirds"

### Leading Lines
- "Path leading from foreground to background"
- "Railroad tracks creating depth and perspective"
- "Architectural lines guiding the eye"

### Symmetry and Balance
- "Symmetrical composition with centered subject"
- "Asymmetric balance with visual weight on the right"
- "Radial symmetry from center point"

### Depth and Layering
- "Foreground, midground, and background clearly defined"
- "Layered composition with depth cues"
- "Shallow depth of field isolating subject from background"

## Lighting Scenarios

### Natural Lighting
- **Golden Hour**: "Warm golden hour lighting, long shadows, soft directional light"
- **Blue Hour**: "Cool blue hour lighting, twilight atmosphere, ambient glow"
- **Midday**: "Bright midday sun, high contrast, minimal shadows"
- **Overcast**: "Soft diffused overcast lighting, even illumination, no harsh shadows"

### Artificial Lighting
- **Studio**: "Professional studio lighting, softbox setup, even illumination"
- **Neon**: "Vibrant neon lighting, colorful glow, urban night atmosphere"
- **Candlelight**: "Warm candlelight, flickering shadows, intimate atmosphere"
- **LED**: "Cool LED lighting, modern aesthetic, crisp illumination"

### Dramatic Lighting
- **Chiaroscuro**: "Strong chiaroscuro, dramatic light and shadow contrast"
- **Rim Lighting**: "Rim lighting outlining subject, backlit silhouette"
- **Rembrandt**: "Rembrandt lighting pattern, triangle of light on cheek"
- **Split Lighting**: "Split lighting, half face in light, half in shadow"

## Color Theory Application

### Color Harmonies

**Complementary:**
- "Complementary orange and blue color palette"
- "Red and green accents creating visual contrast"

**Analogous:**
- "Analogous blue, teal, and green tones"
- "Warm analogous colors: yellow, orange, red"

**Triadic:**
- "Triadic color scheme: red, yellow, blue"
- "Primary color palette with balanced distribution"

**Monochromatic:**
- "Monochromatic blue tones with varying saturation"
- "Single hue palette with light and dark variations"

### Color Psychology
- "Calming cool tones: blues and greens"
- "Energetic warm tones: reds and oranges"
- "Sophisticated neutral palette: grays and beiges"
- "Vibrant high-saturation colors for energy"

## Troubleshooting Common Issues

### Issue: Wrong Style Despite Style Keywords

**Solutions:**
- Add more specific style descriptors
- Use negative prompts to exclude unwanted styles
- Reference specific artists or movements: "in the style of [artist]"
- Combine style with medium: "digital illustration, minimalist style"

### Issue: Missing Key Details

**Solutions:**
- Add explicit detail markers: "with visible [detail]", "featuring [element]"
- Use emphasis syntax if supported: `((important detail))`
- Break down complex subjects into component parts
- Add detail to negative prompt: "not missing [detail]"

### Issue: Unwanted Elements Keep Appearing

**Solutions:**
- Strengthen negative prompts with specific exclusions
- Be more explicit about what SHOULD appear (reduces ambiguity)
- Add context that naturally excludes unwanted elements
- Use multiple negative prompt variations

### Issue: Inconsistent Quality

**Solutions:**
- Add quality markers: "high resolution", "detailed", "professional"
- Specify technical specs: "4K", "sharp focus", "crisp details"
- Include rendering hints: "studio quality", "commercial photography"
- Use negative prompts: "low quality", "blurry", "pixelated"

### Issue: Wrong Composition

**Solutions:**
- Add explicit camera/lens specifications
- Describe framing: "close-up", "wide shot", "medium shot"
- Specify angle: "low angle", "bird's eye view", "eye level"
- Mention composition rules: "rule of thirds", "centered", "asymmetric"

### Issue: Wrong Mood/Atmosphere

**Solutions:**
- Add explicit mood keywords early in prompt
- Describe lighting that supports the mood
- Include color palette that conveys the emotion
- Use negative prompts to exclude opposite moods

## Prompt Templates by Use Case

### E-commerce Product Photography

```
[Product name] with [specific features], displayed on [surface/material], [lighting setup], [composition: angle, framing], professional product photography style, [color palette], high resolution, clean background

Negative prompt: shadows, reflections, text, watermarks, people, hands, cluttered background
```

### Social Media Content

```
[Subject], [style: illustration/photorealistic/3D], [color palette], [mood], [composition], optimized for [platform: Instagram square/Story/TikTok vertical], eye-catching and shareable, high resolution

Negative prompt: text overlays, watermarks, low quality, blurry
```

### Brand Identity Visuals

```
[Subject/concept], [brand aesthetic: minimalist/modern/vintage], [brand colors], [style], [mood that matches brand], professional brand photography/illustration, consistent with [brand name] visual identity, high resolution

Negative prompt: competing styles, off-brand colors, unprofessional
```

### Editorial/Article Illustrations

```
[Subject/concept], editorial illustration style, [artistic medium], [color palette], [mood], [composition], suitable for print/digital publication, high resolution, professional

Negative prompt: low quality, watermarks, text, distracting elements
```

### Concept Art/Design Exploration

```
[Subject/concept], concept art style, [artistic direction], [color exploration], [mood], [composition], detailed, high resolution, exploration of [specific aspect: lighting/materials/composition]

Negative prompt: final polished render, photorealistic (if exploring stylized), low detail
```

### Portrait Photography

```
Portrait of [subject description], [clothing/style], [expression], shot with [lens type], [lighting setup], [background], [mood], professional portrait photography, high resolution

Negative prompt: casual setting, harsh shadows, low quality, unprofessional, distracting background
```

### Architectural Visualization

```
[Building/structure description], [architectural style], [time of day/lighting], [camera angle and lens], [surrounding environment], architectural visualization, photorealistic 3D render, high resolution

Negative prompt: people, vehicles, text, signs, low quality, unrealistic materials
```

### Nature/Landscape Photography

```
[Landscape description], [time of day/lighting], [weather conditions], [camera specs], [composition], [mood], nature photography, photorealistic, high resolution

Negative prompt: people, buildings, vehicles, text, watermarks, artificial elements
```

## Advanced Composition Keywords

### Camera Movements
- "Tracking shot", "dolly shot", "crane shot", "handheld camera"

### Film Techniques
- "Cinematic", "film grain", "anamorphic lens", "letterbox format"

### Visual Effects
- "Motion blur", "depth of field", "bokeh", "lens flare", "chromatic aberration"

### Post-Processing Styles
- "Color graded", "high contrast", "desaturated", "vibrant saturation", "film look"

## Iterative Refinement Workflow

1. **Version 1**: Basic subject + style
2. **Version 2**: Add composition and framing
3. **Version 3**: Add visual details (colors, textures, lighting)
4. **Version 4**: Add mood and atmosphere
5. **Version 5**: Add technical specs
6. **Version 6**: Add negative prompts
7. **Version 7+**: Fine-tune based on outputs

Document what changes between versions and their impact on results.

