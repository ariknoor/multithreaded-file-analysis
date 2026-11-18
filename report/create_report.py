
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
    "In this project, I developed a file analyzer in C and compared "
    "two ways of processing files: sequentially and with multiple threads. "
    "The program searches text files for a target string and counts how "
    "many times it appears. The sequential analyzer checks the files one "
    "by one, whereas the multithreaded analyzer shares the work among "
    "POSIX threads."
)
paragraph(
    "I also created a separate example to show how a race condition "
    "can occur when multiple threads update the same counter. A mutex "
    "was then used to protect the shared counter and produce the correct "
    "result. To compare performance, I tested small, medium, and large "
    "datasets with different thread counts. Each configuration was run "
    "five times, and the average execution time, speedup, and efficiency "
    "were calculated."
)

heading("1. Introduction")
paragraph(
    "Multithreading allows a program to work on more than one task at "
    "a time by using multiple threads. When tasks can be handled "
    "independently, dividing the work among threads may reduce the time "
    "needed to finish it. However, problems can occur when threads access "
    "and update the same shared data without proper synchronization. "
    "This can lead to race conditions and incorrect results."
)
paragraph(
    "I used a file-analysis application to explore these ideas in "
    "practice. The project compares the time taken by sequential and "
    "multithreaded file processing. It also includes a race-condition "
    "example and shows how a POSIX mutex can protect shared data."
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



# -------------------------------------------------
# IMPLEMENTATION
# -------------------------------------------------
heading("4. System Design and Implementation")

heading("4.1 Sequential File Analyzer", 2)
paragraph(
    "The sequential analyzer checks the input files one by one. It opens "
    "each file, reads it line by line, searches for the target string, "
    "and counts every match. After processing the files, it displays "
    "the count for each file and the overall total."
)
paragraph(
    "For file reading, the program uses the C function fgets(). It uses "
    "strstr() to search each line for the target string. This means it "
    "counts substring matches; it does not check whether the target "
    "appears as a separate complete word."
)

heading("4.2 Multithreaded File Analyzer", 2)
paragraph(
    "The multithreaded analyzer uses POSIX pthreads to handle files "
    "concurrently. The program divides the input files into ranges and "
    "assigns each range to a worker thread. Each worker processes its "
    "assigned files and stores the counts in its own result entries."
)
paragraph(
    "After creating the workers, the main thread uses pthread_join() "
    "to wait until they finish. It then combines the results from all "
    "files. Each worker writes to separate result entries, so the file "
    "counting process does not need a shared global counter protected "
    "by a mutex."
)
add_bullet("Thread counts tested: 1, 2, 4, and 8.")
add_bullet("Maximum supported thread count in the application: 8.")
add_bullet("Maximum file capacity in the implementation: 10.")

heading("4.3 Race Condition Demonstration", 2)
paragraph(
    "To demonstrate a race condition, I created a separate program "
    "with two threads that update the same counter. Each thread performs "
    "1,000,000 increments, so the expected final value is 2,000,000. "
    "Without synchronization, both threads can access the counter at "
    "the same time. As a result, some updates may be lost and the final "
    "value may be lower than expected."
)
paragraph(
    "The actual counter value was different from the expected value "
    "in the test runs, and it may change from one execution to another. "
    "In C, a data race causes undefined behavior, so a particular "
    "incorrect result cannot be guaranteed every time."
)

heading("4.4 Mutex Solution", 2)
paragraph(
    "I fixed the shared-counter problem by using a pthread mutex. "
    "Before changing the counter, a thread locks the mutex. It unlocks "
    "the mutex after completing the update. This allows only one thread "
    "at a time to enter the protected critical section. With this "
    "synchronization, the final counter value was 2,000,000, as expected."
)

heading("5. Testing and Dataset")
paragraph(
    "I prepared three datasets to test the analyzer with different "
    "amounts of input. Each dataset contains eight text files, and "
    "WARNING was used as the target string. The files were arranged so "
    "that each line contains one matching occurrence. This makes it "
    "possible to check the program's total count against the expected "
    "number of lines."
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
    "I tested both analyzers with the prepared datasets. The tests "
    "included multithreaded runs using 1, 2, 4, and 8 threads, as well "
    "as the race-condition and mutex examples. I also checked how the "
    "program responds to an invalid thread count, a missing file, and "
    "a target string that does not appear in the input."
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



# -------------------------------------------------
# PERFORMANCE
# -------------------------------------------------
heading("6. Performance Evaluation")

heading("6.1 Measurement Method", 2)
paragraph(
    "I measured execution time using the Linux date command with "
    "nanosecond timestamps. During each run, the program output was "
    "sent to /dev/null so it would not appear in the terminal. I ran "
    "every configuration five times and calculated the average "
    "execution time from those results."
)
paragraph(
    "The recorded time covers the complete command execution. This "
    "includes starting the program and, for the multithreaded version, "
    "creating the threads. I used the same timing approach for both "
    "versions so that their results could be compared consistently."
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
    "The graphs below show how execution time changed with different "
    "thread counts for the small, medium, and large datasets."
)
add_image(
    "performance_graph.png",
    "Figure 1: Combined performance comparison."
)
add_image(
    "small_performance.png",
    "Figure 2: Performance results for the small dataset."
)

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
    "On the small dataset, using two threads gave the best result, "
    "with an average execution time of 8.483 ms. Using eight threads "
    "did not make the program faster. This suggests that, for a small "
    "amount of work, the extra cost of creating and managing more "
    "threads can reduce the benefit of multithreading."
)
paragraph(
    "The medium dataset gave its best result with eight threads, "
    "taking an average of 22.693 ms. The four-thread version was also "
    "faster than the sequential version in this test."
)
paragraph(
    "For the large dataset, eight threads produced the lowest average "
    "execution time of 24.268 ms. In these measurements, using more "
    "threads was more beneficial for the larger workload than it was "
    "for the small dataset."
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
    "The results in this table are based on tests performed on the "
    "current computer. Performance may be different on another system "
    "because hardware and background activity can affect execution "
    "time. The speedup above 2 for the small dataset is the measured "
    "result from these runs; measurement variation may have influenced it."
)



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
    "Through this project, I developed and tested both sequential and "
    "multithreaded file analyzers using C and POSIX threads. The "
    "multithreaded version divided the input files among worker threads "
    "and combined their results after they finished. The functional "
    "tests produced the expected occurrence counts for all three "
    "prepared datasets."
)
paragraph(
    "The race-condition test showed that two threads updating the "
    "same counter without synchronization can produce an incorrect "
    "result. Using a mutex solved this problem and gave the expected "
    "counter value. The benchmark results also showed that multithreading "
    "can improve execution time, especially for larger datasets. However, "
    "the best number of threads depends on the amount of work and the "
    "overhead of managing those threads."
)

heading("9. References")

def add_hyperlink(paragraph, text, url):
    part = paragraph.part
    relationship_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True
    )

    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), relationship_id)

    run = OxmlElement("w:r")
    properties = OxmlElement("w:rPr")

    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    properties.append(color)

    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    properties.append(underline)

    run.append(properties)

    text_element = OxmlElement("w:t")
    text_element.text = text
    run.append(text_element)

    hyperlink.append(run)
    paragraph._p.append(hyperlink)


references = [
    ("Linux man-pages: POSIX Threads (pthreads)",
     "https://man7.org/linux/man-pages/man7/pthreads.7.html"),
    ("GNU Compiler Collection (GCC) Documentation",
     "https://gcc.gnu.org/onlinedocs/"),
    ("Python Official Documentation",
     "https://docs.python.org/3/"),
    ("Matplotlib Official Documentation",
     "https://matplotlib.org/stable/")
]

for title, url in references:
    p_ref = doc.add_paragraph(style="List Number")
    add_hyperlink(p_ref, title, url)

heading("Appendix A: Project Evidence")
paragraph(
    "The project folder contains the C source files, test datasets, "
    "benchmark results in CSV format, performance graphs, test cases, "
    "and screenshots showing the program executions. All collected "
    "screenshots are kept in the results/screenshots/ folder."
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
