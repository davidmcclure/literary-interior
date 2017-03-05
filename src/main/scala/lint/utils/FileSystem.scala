

package lint.utils

import java.io.File


object FileSystem {

  /* List a directory recursively.
   */
  def walkTree(f: File): Iterable[File] = {

    val children = new Iterable[File] {
      def iterator = {
        if (f.isDirectory) f.listFiles.iterator
        else Iterator.empty
      }
    }

    Seq(f) ++: children.flatMap(walkTree(_))

  }

}
