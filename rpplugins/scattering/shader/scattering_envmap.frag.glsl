/**
 *
 * RenderPipeline
 *
 * Copyright (c) 2014-2016 tobspr <tobias.springer1@gmail.com>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 */

#version 430


#pragma include "render_pipeline_base.inc.glsl"

layout(r11f_g11f_b10f) uniform imageCube RESTRICT DestCubemap;

#pragma include "scattering_method.inc.glsl"
#pragma include "merge_scattering.inc.glsl"

void main() {

    // Get cubemap coordinate
    int texsize = imageSize(DestCubemap).x;
    ivec2 coord = ivec2(gl_FragCoord.xy);

    // Get cubemap view_vector
    ivec2 clamped_coord; int face;
    vec3 view_vector = texcoord_to_cubemap(texsize, coord, clamped_coord, face);

    // Store horizon
    float horizon = view_vector.z;

    vec3 orig_view_vector = view_vector;
    view_vector.z = max(view_vector.z, 0.0);

    // Get inscattered light
    vec3 result_scattering = vec3(0);
    vec3 result_sun_color = vec3(0);
    do_scattering(view_vector * 1e10, view_vector, result_scattering, result_sun_color);

    imageStore(DestCubemap, ivec3(clamped_coord, face), vec4(result_scattering, 1.0));
}
