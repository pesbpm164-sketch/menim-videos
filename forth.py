from manim import *
import numpy as np

class DetailedInclineSimulation(Scene):
    def construct(self):
        base_len = 5.5
        height = 2.2
        interior = np.arctan(height / base_len)
        
        origin = LEFT*3.5 + DOWN*1.8
        base_end = origin + RIGHT*base_len
        top = origin + UP*height

        base = Line(origin, base_end, color=WHITE, stroke_width=4)
        incline = Line(top, base_end, color=BLUE, stroke_width=10)
        left_wall = Line(origin, top, color=WHITE, stroke_width=2)
        left_wall.set_opacity(0.15)

        # CLEAN TITLE - no "No Overlap"
        title = Text("Object on an Inclined Plane", font_size=32).to_edge(UP, buff=0.4)

        arc = Arc(radius=0.6, start_angle=PI - interior, angle=interior, color=YELLOW, stroke_width=5)
        arc.move_arc_center_to(base_end)
        theta_label = MathTex(r"\theta", color=YELLOW).scale(0.9).move_to(base_end + LEFT*1.0 + UP*0.2)

        block_size = 0.6
        incline_angle = np.arctan2(-height, base_len)
        def point_on_incline(t):
            return top + (base_end - top) * t
        norm = np.array([height, base_len, 0])
        norm = norm / np.linalg.norm(norm)
        offset = norm * 0.32
        start_pos = point_on_incline(0.15) + offset

        block = Square(side_length=block_size, color=RED, fill_opacity=0.9).rotate(incline_angle).move_to(start_pos)

        self.play(Write(title))
        self.play(Create(base), Create(incline), Create(left_wall), Create(arc), Write(theta_label), FadeIn(block), run_time=1.5)

        # MG - WHITE solid, label FAR LEFT to avoid blue line
        mg_arrow = Arrow(block.get_center(), block.get_center() + DOWN*1.6, color=WHITE, buff=0, stroke_width=8)
        mg_label = MathTex(r"\vec{W}=mg", color=WHITE).scale(0.85)
        mg_label.move_to(block.get_center() + LEFT*1.8 + DOWN*0.3)  # FAR LEFT, not near blue

        self.play(Create(mg_arrow), Write(mg_label), run_time=1)

        # Dotted components
        incline_unit = (base_end - top) / np.linalg.norm(base_end - top)
        perp_unit = -norm

        # Parallel - orange dotted along incline
        mg_parallel = DashedLine(block.get_center(), block.get_center() + incline_unit*1.2, color=ORANGE, stroke_width=6, dash_length=0.12)
        mg_parallel.add_tip(tip_length=0.2)
        # Label in EMPTY SPACE below blue line, to the right
        mg_parallel_label = MathTex(r"mg\sin\theta", color=ORANGE).scale(0.8)
        mg_parallel_label.move_to(block.get_center() + RIGHT*2.5 + DOWN*1.2)  # FAR RIGHT, well below blue line

        # Perpendicular - green dotted into incline
        mg_perp = DashedLine(block.get_center(), block.get_center() + perp_unit*1.1, color=GREEN, stroke_width=6, dash_length=0.12)
        mg_perp.add_tip(tip_length=0.2)
        # Label FAR LEFT, away from W=mg
        mg_perp_label = MathTex(r"mg\cos\theta", color=GREEN).scale(0.8)
        mg_perp_label.move_to(block.get_center() + LEFT*2.8 + DOWN*0.8)  # FAR FAR LEFT, not overlapping W=mg

        dotted_h = DashedLine(block.get_center() + incline_unit*1.2, block.get_center() + incline_unit*1.2 + perp_unit*1.1, color=WHITE, stroke_width=2, dash_length=0.08, stroke_opacity=0.3)
        dotted_v = DashedLine(block.get_center() + perp_unit*1.1, block.get_center() + incline_unit*1.2 + perp_unit*1.1, color=WHITE, stroke_width=2, dash_length=0.08, stroke_opacity=0.3)

        self.play(Create(mg_parallel), Write(mg_parallel_label), run_time=1)
        self.play(Create(mg_perp), Write(mg_perp_label), Create(dotted_h), Create(dotted_v), run_time=1)

        # Normal - blue solid, label TOP
        n_arrow = Arrow(block.get_center(), block.get_center() + norm*1.2, color=BLUE, buff=0, stroke_width=8)
        n_label = MathTex(r"\vec{N}=mg\cos\theta", color=BLUE).scale(0.8)
        n_label.move_to(block.get_center() + UP*1.8)  # TOP, free space

        self.play(Create(n_arrow), Write(n_label), run_time=1)

        # Friction - yellow solid, label FAR LEFT TOP
        friction = Arrow(block.get_center(), block.get_center() - incline_unit*1.0, color=YELLOW, buff=0, stroke_width=8)
        friction_label = MathTex(r"\vec{f}_k=\mu_k N", color=YELLOW).scale(0.8)
        friction_label.move_to(block.get_center() + LEFT*2.5 + UP*1.0)  # FAR LEFT TOP, not overlapping mg cos

        self.play(Create(friction), Write(friction_label), run_time=1)

        # Bottom equations - clear, in free space
        bottom_eq = VGroup(
            MathTex(r"F_{net}=mg\sin\theta-\mu_k mg\cos\theta", color=WHITE).scale(0.65),
            MathTex(r"a=g(\sin\theta-\mu_k\cos\theta)", color=GREEN).scale(0.75),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)

        self.play(Write(bottom_eq), run_time=1.5)
        self.wait(1)

        self.play(FadeOut(dotted_h), FadeOut(dotted_v))

        tracker = ValueTracker(0.15)
        moving_block = always_redraw(lambda: Square(side_length=block_size, color=RED, fill_opacity=0.9).rotate(incline_angle).move_to(point_on_incline(tracker.get_value()) + offset))
        moving_mg = always_redraw(lambda: Arrow(point_on_incline(tracker.get_value()) + offset, point_on_incline(tracker.get_value()) + offset + DOWN*1.2, color=WHITE, buff=0, stroke_width=5, stroke_opacity=0.7))
        moving_n = always_redraw(lambda: Arrow(point_on_incline(tracker.get_value()) + offset, point_on_incline(tracker.get_value()) + offset + norm*0.8, color=BLUE, buff=0, stroke_width=5, stroke_opacity=0.7))
        moving_f = always_redraw(lambda: Arrow(point_on_incline(tracker.get_value()) + offset, point_on_incline(tracker.get_value()) + offset - incline_unit*0.5, color=YELLOW, buff=0, stroke_width=5, stroke_opacity=0.7))

        self.add(moving_block, moving_mg, moving_n, moving_f)
        self.remove(block, mg_arrow, n_arrow, friction, mg_parallel, mg_perp)
        self.play(FadeOut(mg_label), FadeOut(mg_parallel_label), FadeOut(mg_perp_label), FadeOut(n_label), FadeOut(friction_label))

        self.play(tracker.animate.set_value(0.8), run_time=5, rate_func=rate_functions.ease_in_quad)
        self.remove(moving_block, moving_mg, moving_n, moving_f)
        final_block = Square(side_length=block_size, color=RED, fill_opacity=0.9).rotate(incline_angle).move_to(point_on_incline(0.8) + offset)
        self.add(final_block)
        self.wait(1)
