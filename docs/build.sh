#!/bin/bash

# ----------------------------------------------------------------------
# FILE: build.sh
# DESCRIPTION: Script to build pixelscan documentation web pages.
# REQUIREMENTS: python 2.7, sphinx 1.3.5
# ----------------------------------------------------------------------

CURDIR=$(readlink -f $(dirname ${BASH_SOURCE[0]}))
PARENTDIR=$(readlink -f $(dirname $CURDIR))
OUTPUTDIR=$CURDIR/api
PIXELSCANDIR=$PARENTDIR
ROOTDIR=$CURDIR

# ==================================================
# Display usage
# --------------------------------------------------
__usage()
{
    echo "Usage: $0 [-h] [-o <directory>] [-p <directory>] [-r <directory>]"
    echo "    -h = Display this usage"
    echo "    -o = output directory"
    echo "    -p = pixelscan directory"
    echo "    -r = root directory"
}

# ==================================================
# Parse arguments
# --------------------------------------------------
while getopts :ho:p:r: flag ; do
    case $flag in
        h) __usage; exit 0; ;;
        o) OUTPUTDIR=$OPTARG; ;;
        p) PIXELSCANDIR=$OPTARG; ;;
        r) ROOTDIR=$OPTARG; ;;
        *) echo "Invalid option: -$OPTARG" >&2; exit 1; ;;
    esac
done
shift $((OPTIND-1))
SOURCEDIR=$ROOTDIR/source/

# ==================================================
# Generate configuration files in source directory
# --------------------------------------------------
sphinx-quickstart \
    --author="Daniel Pulido" \
    --dot=_ \
    --ext-autodoc \
    --ext-ifconfig \
    --ext-intersphinx \
    --language=en \
    --master=index \
    --no-batchfile \
    --no-makefile \
    --no-use-make-mode \
    --project=pixelscan \
    --quiet \
    --release=0.3.2 \
    --sep \
    --suffix=.rst \
    -v 0.3.2 \
    $ROOTDIR

# ==================================================
# Build API documents
# --------------------------------------------------
PYTHONPATH=$PIXELSCANDIR sphinx-apidoc -e -f -o $SOURCEDIR $PIXELSCANDIR/pixelscan

# ==================================================
# Update conf.py with bootstrap theme
# --------------------------------------------------
echo "" >> $SOURCEDIR/conf.py
echo "import sphinx_bootstrap_theme" >> $SOURCEDIR/conf.py
echo "autoclass_content = 'both'" >> $SOURCEDIR/conf.py
echo "html_theme = 'bootstrap'" >> $SOURCEDIR/conf.py
echo "html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()" >> $SOURCEDIR/conf.py
echo "html_show_sourcelink = False" >> $SOURCEDIR/conf.py

# ==================================================
# Update index.rst with content
# --------------------------------------------------
cp $CURDIR/intro.txt $SOURCEDIR
sed -i "s/Welcome to pixelscan's documentation!/**pixelscan**/g" $SOURCEDIR/index.rst
sed -i "/Content/i\\
.. include:: intro.txt\n" $SOURCEDIR/index.rst
sed -i "s/Contents:/Contents\n==================/g" $SOURCEDIR/index.rst
sed -i "s/:maxdepth: 2/:maxdepth: 1/g" $SOURCEDIR/index.rst
sed -i "/:maxdepth: 1/a\\
\\
   modules.rst\\
   pixelscan.pixelscan.rst" $SOURCEDIR/index.rst

# ==================================================
# Build html documents
# --------------------------------------------------
PYTHONPATH=$PIXELSCANDIR sphinx-build $SOURCEDIR $OUTPUTDIR

# ==================================================
# Add file to disable github jekyll processing
# --------------------------------------------------
touch $OUTPUTDIR/.nojekyll

# ==================================================
# Clean up build directories
# --------------------------------------------------
rm -rf $SOURCEDIR
rm -rf $ROOTDIR/build/