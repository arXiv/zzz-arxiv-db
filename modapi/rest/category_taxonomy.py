"""category taxonomy"""

from  fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from modapi.auth import User, auth_user
import requests

from pydantic import BaseModel

from modapi.tables.arxiv_models import (
    ArchiveGroup,
    ArchiveDef,
    Archives,
    ArchiveCategory
)

from sqlalchemy import select, or_, and_, text
from sqlalchemy.orm import joinedload


import logging

log = logging.getLogger(__name__)

router = APIRouter()


async def active_option_categories(archive_id: str):
    async with Session() as session:
        stmt = (select(ArchiveCategory)
                .join(CategoryDef,
                      ArchiveCategory.category_id == CategoryDef.category)
                .options(joinedload(CategoryDev))
                .filter(ArchiveCategory.archive_id=archive_id)
                .filter(active == 1)
                .order_by(ArchiveCategory.category_id))
        res = await session.execute(stmt)
        return res.all()
        
    
@router.get("/category_taxonomy")
async def category_taxonomy():
    """Gets the arXiv category taxonomy"""

    archive_data = {}

    async with Session() as session:
        res = await session.execute(select(ArchiveGroup)
                                    .filter(ArchiveGroup.group_id != 'test'))
        for row in res.all():
            id = row.group_id
            archive_data[id] = {
                'group': id,
                'name' : group_name,
                'archives': []
                }

        res = await session.execute(select(Archives)
                                    .fitler(Archives.end_date == '')
                                    .filter(Archives.archive_id != 'test')
                                    order_by(Archives.archive_id))

        for row in res.all():
            short, group = (row.archive_id, row.in_group)
            categories = active_option_categories(short)
            if categories:
                subgroup_data = {
                    'archive' = row.archive_id,
 		    'name' = row.archive_name,
 		    'categories' = []
                }
                for cat in categories:
                    
# 		    
                
# 	while ( my $archive = $archives->next ) {

# 		my $archive_short = $archive->archive_id;
# 		my $archive_group = $archive->get_column('in_group');
		
# 		my $categories = $archive->active_option_categories->search( {},
# 			{ order_by => 'category' } );
# 		if ( $categories && $categories->count > 0 ) {

# 			my $subgroup_data = {
# 				archive => $archive->archive_id,
# 				name => $archive->archive_name,
# 				categories => []
# 			};

# 			while ( my $category = $categories->next ) {
# 				my $cat = $category->category;

# 				# Ensure the category shows up under the canonical archive
# 				next if ( $archive_short ne get_archive_from_category($cat) );

# 				my $cat_data = { category => $cat, name => $category->name };
# 				if ( defined $opts->{extended} ) {
# 					# include extended category descriptions
# 					my ($a, $sc) = split(/\./, $cat);
# 					$cat_data->{description} = $Subj_class_description{$a}{$sc} ? $Subj_class_description{$a}{$sc} : '';
# 				}
# 				push @{ $subgroup_data->{categories} }, $cat_data;
# 			}
			
# 			push @{ $archive_data->{$archive_group}->{archives} }, $subgroup_data;
# 		}

# 	}

# 	foreach ( sort keys %{$archive_data} ) {
# 		push @{$data}, $archive_data->{$_};
# 	}

# 	return { groups => $data };
# }
