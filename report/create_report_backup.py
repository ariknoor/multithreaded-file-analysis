
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.style import WD_STYLE_TYPE
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RESULTS = BASE / "results"
OUTPUT = BASE / "report" / "technical_report.docx"

doc = Document()

# Page setup
section = doc.sections[0]
section.top_margin = Inches(0.75)
section.bottom_margin = Inches(0.75)
section.left_margin = Inches(0.85)
section.right_margin = Inches(0.85)

# Default font
styles = doc.styles
styles["Normal"].font.name = "Arial"
styles["Normal"].font.size = Pt(10)
styles["Normal"].paragraph_format.space_after = Pt(6)

for style_name in ["Heading 1", "Heading 2", "Heading 3"]:
    styles[style_name].font.name = "Arial"
    styles[style_name].font.color.rgb = RGBColor(31, 78, 121)

styles["Heading 1"].font.size = Pt(17)
styles["Heading 2"].font.size = Pt(13)
styles["Heading 3"].font.size = Pt(11)

# Header and footer
header = section.header.paragraphs[0]
header.text = "MULTITHREADED FILE ANALYSIS AND PERFORMANCE EVALUATION"
header.alignment = WD_ALIGN_PARAGRAPH.CENTER
header.runs[0].font.size = Pt(8)
header.runs[0].font.color.rgb = RGBColor(100, 100, 100)

footer = section.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
footer.add_run("Technical Report | Page ").font.size = Pt(8)

field = OxmlElement("w:fldSimple")
field.set(qn("w:instr"), "PAGE")
footer._p.append(field)


def shade_cell(cell, fill="D9EAF7"):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def add_table(headers, rows):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    for i, header_text in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = str(header_text)
        shade_cell(cell)
        for run in cell.paragraphs[0].runs:
            run.bold = True
            run.font.size = Pt(9)

    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = str(value)
            cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            for paragraph in cells[i].paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(8.5)

    doc.add_paragraph()
    return table


def add_bullet(text):
    doc.add_paragraph(text, style="List Bullet")


def add_number(text):
    doc.add_paragraph(text, style="List Number")


def add_image(filename, caption, width=5.8):
    path = RESULTS / filename
    if path.exists():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(path), width=Inches(width))
        cap = doc.add_paragraph(caption)
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in cap.runs:
            run.italic = True
            run.font.size = Pt(9)
    else:
        doc.add_paragraph(
            f"[Graph not found: results/{filename}]"
        )


def heading(text, level=1):
    doc.add_heading(text, level=level)


def paragraph(text):
    doc.add_paragraph(text)


# -------------------------------------------------
# COVER PAGE
# -------------------------------------------------
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(55)
r = p.add_run("UNIVERSITY OF FRONTIER TECHNOLOGY, BANGLADESH")
r.bold = True
r.font.size = Pt(18)
r.font.color.rgb = RGBColor(31, 78, 121)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("[Department Name]").font.size = Pt(12)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(55)
r = p.add_run("TECHNICAL REPORT")
r.bold = True
r.font.size = Pt(20)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(15)
r = p.add_run(
    "Multithreaded File Analysis and\nPerformance Evaluation"
)
r.bold = True
r.font.size = Pt(16)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(45)
p.add_run("Submitted By\n").bold = True
p.add_run("[Student Name]\n")
p.add_run("Student ID: [Student ID]\n")
p.add_run("Course Code: [Course Code]\n")
p.add_run("Course Title: [Course Title]\n")

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(25)
p.add_run("Submitted To\n").bold = True
p.add_run("[Instructor Name]\n")
p.add_run("[Designation]\n")

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(35)
p.add_run("Submission Date: [Enter Date]")

doc.add_page_break()

# -------------------------------------------------
# ABSTRACT
# -------------------------------------------------
heading("Abstract")
paragraph(
    "This project implements and evaluates a file-analysis application "
    "using sequential and multithreaded programming in the C language. "
    "The application searches multiple text files for a target string "
    "and counts its occurrences. The sequential version processes files "
    "one after another, while the multithreaded version distributes file "
    "processing among POSIX threads."
)
paragraph(
    "The project also demonstrates a race condition through concurrent "
    "updates to a shared counter and presents a mutex-based solution. "
    "Performance was measured using small, medium, and large datasets "
    "with different thread counts. Five measurements were collected for "
    "each configuration, and average execution time, speedup, and "
    "efficiency were calculated."
)

heading("1. Introduction")
paragraph(
    "Modern computer systems support concurrent execution through "
    "multithreading. A multithreaded program can divide independent work "
    "among multiple threads, potentially reducing execution time. "
    "However, concurrent access to shared data can introduce race "
    "conditions and incorrect results."
)
paragraph(
    "This project explores these concepts through a practical file "
    "analysis application. It compares sequential processing with "
    "multithreaded processing and demonstrates synchronization using "
    "POSIX mutexes."
)

heading("2. Objectives")
for item in [
    "Develop a sequential file analyzer in C.",
    "Develop a multithreaded file analyzer using POSIX pthreads.",
    "Distribute file-processing tasks among multiple threads.",
    "Demonstrate a race condition involving a shared counter.",
    "Prevent the race condition using a mutex.",
    "Measure performance using different dataset sizes and thread counts.",
    "Calculate average execution time, speedup, and efficiency.",
    "Present performance results using graphs."
]:
    add_bullet(item)

heading("3. Tools and Technologies")
add_table(
    ["Tool / Technology", "Purpose"],
    [
        ["C Programming Language", "Implementation of file analyzers"],
        ["POSIX Pthreads", "Thread creation and synchronization"],
        ["GCC", "Compilation of C programs"],
        ["Ubuntu Linux", "Development and testing environment"],
        ["Python", "Benchmark data processing and graph generation"],
        ["Matplotlib", "Performance graph generation"],
        ["ONLYOFFICE", "Editing the final report"]
    ]
)

doc.add_page_break()

# -------------------------------------------------
# IMPLEMENTATION
# -------------------------------------------------
heading("4. System Design and Implementation")

heading("4.1 Sequential File Analyzer", 2)
paragraph(
    "The sequential analyzer processes the supplied files one at a time. "
    "It opens each file, reads its contents line by line, searches for "
    "the target string, and counts matching occurrences. The result for "
    "each file is displayed, followed by the total occurrence count."
)
paragraph(
    "The implementation uses standard C file handling functions such "
    "as fgets() and string searching with strstr(). Therefore, the "
    "program counts substring matches rather than restricting matches "
    "to complete words."
)

heading("4.2 Multithreaded File Analyzer", 2)
paragraph(
    "The multithreaded analyzer uses POSIX pthreads to process multiple "
    "files concurrently. The input files are divided into separate "
    "ranges and assigned to worker threads. Each thread processes its "
    "assigned files and stores results in its designated result entries."
)
paragraph(
    "The main thread waits for worker threads using pthread_join() "
    "before combining the individual file counts. Since each worker "
    "updates separate result entries, the main counting operation does "
    "not require a shared global counter protected by a mutex."
)
add_bullet("Thread counts tested: 1, 2, 4, and 8.")
add_bullet("Maximum supported thread count in the application: 8.")
add_bullet("Maximum file capacity in the implementation: 10.")

heading("4.3 Race Condition Demonstration", 2)
paragraph(
    "A separate demonstration program creates two threads that increment "
    "the same shared counter. Each thread performs 1,000,000 increments. "
    "The expected final value is 2,000,000. Without synchronization, "
    "both threads may read and update the shared variable concurrently. "
    "Some updates can be lost, producing an incorrect result."
)
paragraph(
    "The observed counter value can vary between executions. A data "
    "race in C is undefined behavior, so the exact incorrect value is "
    "not guaranteed."
)

heading("4.4 Mutex Solution", 2)
paragraph(
    "A pthread mutex is used to protect the shared counter. A thread "
    "locks the mutex before updating the counter and unlocks it after "
    "the update. This ensures that only one thread at a time executes "
    "the protected critical section. The expected final counter value "
    "is 2,000,000, and the mutex-protected execution produced that value."
)

heading("5. Testing and Dataset")
paragraph(
    "Three datasets were used to evaluate the analyzer. Each dataset "
    "contains eight text files. The target string was WARNING, and the "
    "test files were prepared so that the total number of matching "
    "occurrences corresponded to the number of lines."
)
add_table(
    ["Dataset", "Files", "Lines per file", "Total occurrences"],
    [
        ["Small", "8", "10,000", "80,000"],
        ["Medium", "8", "50,000", "400,000"],
        ["Large", "8", "100,000", "800,000"]
    ]
)

paragraph(
    "Functional testing covered sequential execution, multithreaded "
    "execution with 1, 2, 4, and 8 threads, race-condition behavior, "
    "mutex synchronization, invalid thread count, missing file, and "
    "a target string with no matches."
)

add_table(
    ["Test ID", "Test description", "Expected / observed outcome"],
    [
        ["TC-01", "Sequential analyzer on small dataset", "80,000 occurrences"],
        ["TC-02 to TC-05", "1, 2, 4, and 8 threads on small dataset", "80,000 occurrences"],
        ["TC-06", "Medium dataset", "400,000 occurrences"],
        ["TC-07", "Large dataset", "800,000 occurrences"],
        ["TC-08", "Race condition demonstration", "Shared counter may be incorrect"],
        ["TC-09", "Mutex solution", "2,000,000 counter value"],
        ["TC-10", "Invalid thread count (0)", "Error message displayed"],
        ["TC-11", "Missing input file", "File-open error displayed"],
        ["TC-12", "No matching target string", "Zero occurrences"]
    ]
)

doc.add_page_break()

# -------------------------------------------------
# PERFORMANCE
# -------------------------------------------------
heading("6. Performance Evaluation")

heading("6.1 Measurement Method", 2)
paragraph(
    "Execution time was measured using the Linux date command with "
    "nanosecond timestamps. The program output was redirected to "
    "/dev/null during timing. Each configuration was executed five "
    "times, and the average was calculated."
)
paragraph(
    "The timing measures the complete command execution, including "
    "program startup and thread creation overhead. The same measurement "
    "approach was used for the sequential and multithreaded programs "
    "to maintain consistency."
)
paragraph(
    "The following formulas were used:"
)
paragraph("Average Execution Time = Sum of measured execution times / Number of runs")
paragraph("Speedup = Sequential average execution time / Parallel average execution time")
paragraph("Efficiency = (Speedup / Number of threads) × 100%")

heading("6.2 Average Execution Time", 2)
add_table(
    ["Dataset", "Sequential (ms)", "1 Thread (ms)", "2 Threads (ms)",
     "4 Threads (ms)", "8 Threads (ms)"],
    [
        ["Small", "19.298", "19.993", "8.483", "13.809", "12.362"],
        ["Medium", "43.928", "46.290", "31.822", "23.559", "22.693"],
        ["Large", "54.084", "60.382", "45.394", "31.383", "24.268"]
    ]
)

heading("6.3 Performance Graphs", 2)
paragraph(
    "The following graphs compare execution time across the tested "
    "thread counts and dataset sizes."
)
add_image(
    "performance_graph.png",
    "Figure 1: Combined performance comparison."
)
add_image(
    "small_performance.png",
    "Figure 2: Performance results for the small dataset."
)
doc.add_page_break()
add_image(
    "medium_performance.png",
    "Figure 3: Performance results for the medium dataset."
)
add_image(
    "large_performance.png",
    "Figure 4: Performance results for the large dataset."
)

heading("6.4 Performance Analysis", 2)
paragraph(
    "For the small dataset, the two-thread configuration achieved the "
    "lowest measured average execution time of 8.483 ms. The eight-thread "
    "configuration was not faster than the two-thread configuration. "
    "This indicates that creating and managing additional threads can "
    "introduce overhead when the workload is relatively small."
)
paragraph(
    "For the medium dataset, the eight-thread configuration achieved "
    "the lowest measured average execution time of 22.693 ms. The "
    "four-thread configuration also improved execution time compared "
    "with sequential processing."
)
paragraph(
    "For the large dataset, the eight-thread configuration achieved "
    "the lowest measured average execution time of 24.268 ms. The "
    "results show that the benefit of additional threads became more "
    "visible as the dataset size increased."
)

heading("6.5 Best Measured Configurations", 2)
add_table(
    ["Dataset", "Best measured configuration", "Average time (ms)",
     "Speedup (approx.)"],
    [
        ["Small", "2 threads", "8.483", "2.275"],
        ["Medium", "8 threads", "22.693", "1.936"],
        ["Large", "8 threads", "24.268", "2.228"]
    ]
)
paragraph(
    "These values represent the measurements collected in this "
    "environment. They should not be interpreted as guaranteed "
    "performance on other computers. The small-dataset speedup above "
    "2 is an observed result and may be influenced by measurement "
    "variation and runtime overhead."
)

doc.add_page_break()

# -------------------------------------------------
# CONCLUSION
# -------------------------------------------------
heading("7. Challenges and Limitations")
for item in [
    "Thread creation and scheduling introduce overhead.",
    "Performance depends on processor hardware, operating system activity, and workload size.",
    "The benchmark measures complete command execution rather than only the file-reading portion.",
    "The analyzer searches for substrings using strstr(), not complete-word matches.",
    "A data race in C has undefined behavior, so race-condition output is not deterministic.",
    "Only three dataset sizes and four multithreaded thread counts were evaluated."
]:
    add_bullet(item)

heading("8. Conclusion")
paragraph(
    "This project demonstrated the development and evaluation of "
    "sequential and multithreaded file analyzers using C and POSIX "
    "threads. The multithreaded implementation divided file-processing "
    "work among worker threads and combined the results after thread "
    "completion. The functional tests confirmed the expected occurrence "
    "counts for the prepared datasets."
)
paragraph(
    "The race-condition experiment showed how concurrent updates to "
    "shared data can produce incorrect results. Applying a mutex "
    "protected the critical section and produced the expected counter "
    "value. The performance evaluation showed that multithreading can "
    "reduce execution time, particularly for larger workloads, although "
    "the best thread count depends on dataset size and execution overhead."
)

heading("9. References")
for item in [
    "The C Programming Language: standard C file handling and string operations.",
    "GNU Compiler Collection (GCC) documentation.",
    "POSIX Threads (pthreads): thread creation, joining, mutex initialization, locking, and unlocking.",
    "Python documentation: https://docs.python.org/3/",
    "Matplotlib documentation: https://matplotlib.org/stable/"
]:
    add_number(item)

heading("Appendix A: Project Evidence")
paragraph(
    "The project directory includes source code, datasets, benchmark "
    "CSV files, generated performance graphs, test cases, and terminal "
    "screenshots. The screenshots are stored in results/screenshots/."
)
for item in [
    "01_combined_performance_graph.png",
    "02_small_performance_graph.png",
    "03_medium_performance_graph.png",
    "04_large_performance_graph.png",
    "05_final_test_execution_results.png",
    "06_race_condition.png",
    "07_mutex_solution.png",
    "09_race_condition_mutex_comparison.png",
    "10_multithreaded_analyzer_test.png",
    "11_sequential_analyzer_test.png"
]:
    add_bullet(item)

# Save document
doc.save(OUTPUT)
print(f"Report created successfully: {OUTPUT}")
