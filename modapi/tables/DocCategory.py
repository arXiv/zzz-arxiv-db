class DocCategory():

    @property 
    def primary(self):
        return next([c for c in self.submission_category if c.is_primary],None)


    '''sub primary_string
{
   my ( $self, $display ) = @_;

   my $primary = $self->primary;
   return unless $primary;
   if ($display)
   {
      return $primary->name . " (" . $primary->category . ")";
   }
   else
   {
      return $primary->category; 
   }

}
'''
    
    @property
    def primary_string(self, display):
        ...

    @property
    def secondaries(self):
        ...
        # sub secondaries
        # {
        #    my ( $self ) = @_;
        #    # $self is a resultset
        #    return $self->search(
        #       { is_primary => { '!=',  1 } },
        #       { order_by => 'category' });
        # }

   @property
   def secondaries_string(self):
       ...
       # sub secondaries_string
       # {
       #    my ( $self, $display ) = @_; 
       
       #    my $string;
       #    my $cats = $self->secondaries;
       #    return '' unless $cats->count > 0;
       #    my $prev = '';
       #    my @cats;
       #    while (my $cat = $cats->next)
       #    {
       #       if( $display )
       #       {
       #          $string .= $prev . $cat->name . 
       #            " (" . $cat->category  . ")";
       #          $prev = ', ';
       #       }
       #       else
       #       {
       #          push @cats, $cat->category;
       #       }
       #    }
       #    return $string if $display;
       #    return join( ' ', sort( @cats ) );
       # }

    @property
    def string(self):
        ...
        # sub string
        # {
        #    my $self = shift;
        
        #    my $sec_string = '';
        #    $sec_string = ' ' . $self->secondaries_string if $self->secondaries_string;
        #    my $primary = $self->primary ? $self->primary->category : '-';
        #    return $primary . $sec_string;
        # }

    @property
    def noprimary_string(self):
        ...
        # sub noprimary_string
        # {
        #    my $self = shift;
        
        #    my $sec_string = '';
        #    $sec_string = ' ' . $self->secondaries_string if $self->secondaries_string;
        #    my $primary = $self->primary ? ('{'.$self->primary->category .'}') : '{no primary}';
        #    return $primary . $sec_string;
        # }


    @property
    highlighted_string(self):
    
        # =head3 highlighted_string()
        
        # Similar to string(), but inserts square brackets around categories that are
        # new, iff the submission/document has one or more categories that are already
    # published. If the submission/document does not have one or more published 
    # category and one or more unpublished category, just return $self->string.
    
    # Order is preserved; primary category appears first and secondaries are ordered
    # lexicographically.
    
    # The brackets are replaced with HTML by the template toolkit.
    
    # =cut


    @property
    def highlighted_string(self):
        ...
    # sub highlighted_string
    # {
    #     my $self = shift;    
    
    #     unless ( $self->search({ is_published => 1 })->count > 0 && 
    #              $self->search({ is_published => 0 })->count > 0) 
    #     {
    #         return $self->string;
    #     }
    
    #     my $primary = $self->primary ? $self->primary->category : '';
    #     if ( $primary && $self->primary->is_published == 0) {
    #         $primary = '[' . $primary . ']';
    #     }
    
    #     my $cats = $self->secondaries;
    #     my $num_sec_cats = $cats->count;
    #     return $primary unless $num_sec_cats > 0;
    
    #     my $sec_string = ' ';   
    #     my %cat_published = ();
    #     while ( my $cat = $cats->next ) 
    #     {
    #         $cat_published{$cat->category} = $cat->is_published ? 1 : 0;       
    #     }
    #     my $count = 0;
    #     foreach my $cat_string ( sort keys %cat_published ) {
    #         $cat_string = '[' . $cat_string . ']' if $cat_published{$cat_string} == 0;
    #         $sec_string .= $cat_string . (++$count < $num_sec_cats ? ' ' : '');
    #     }
    
    #     return $primary . $sec_string;
    # }


    @property
    def highlighted_noprimary_string(self):
        ...
    # =head3 highlighted_noprimary_string()

    # Similar to highlighted_string(), in that it inserts square brackets around 
    # categories that are new, iff the submission/document has one or more categories 
    # that are already published. It also inserts curly brackets around the primary
    # category, which may or may not exist. If there is no primary, it is represented
    # by {no primary}.

    # If the submission/document does not have one or more published 
    # category and one or more unpublished category, just return 
    # $self->noprimary_string.

    # Order is preserved; primary category appears first and secondaries are ordered
    # lexicographically.

    # The square and curly brackets are replaced with HTML by the template toolkit.

    # =cut
    # sub highlighted_noprimary_string
    # {
    #     my $self = shift;    

    #     unless ( $self->search({ is_published => 1 })->count > 0 && 
    #              $self->search({ is_published => 0 })->count > 0) 
    #     {
    #         return $self->noprimary_string;
    #     }

    #     my $primary = $self->primary ? ('{'.$self->primary->category .'}') : '';
    #     if ( $primary && $self->primary->is_published == 0) {
    #         $primary = '[' . $primary . ']';
    #     }

    #     my $cats = $self->secondaries;
    #     my $num_sec_cats = $cats->count;
    #     return $primary unless $num_sec_cats > 0;

    #     my $sec_string = ' ';   
    #     my %cat_published = ();
    #     while ( my $cat = $cats->next ) 
    #     {
    #         $cat_published{$cat->category} = $cat->is_published ? 1 : 0;       
    #     }
    #     my $count = 0;
    #     foreach my $cat_string ( sort keys %cat_published ) {
    #         $cat_string = '[' . $cat_string . ']' if $cat_published{$cat_string} == 0;
    #         $sec_string .= $cat_string . (++$count < $num_sec_cats ? ' ' : '');
    #     }

    #     unless ( defined $primary ) {
    #         $primary = '{no primary}';
    #     }

    #     return $primary . $sec_string;
    # }


    @property
    def display_string(self):
        ...
    # sub display_string
    # {
    #    my $self = shift;
    #    my $sec_string = '';
    #    $sec_string = ', ' . $self->secondaries_string(1) if $self->secondaries_string;
    #    return $self->primary_string(1) . $sec_string;
    # }


    @property
    def fudged_string(self):
        ...
    # sub fudged_string {
    #     my ( $self, $cat_str ) = @_;

    #     $cat_str ||= $self->string;
    #     my @cat_list = split(/ /, $cat_str);
    #     my %cat_hash =  map { $_ => 1 } @cat_list; 

    #     foreach my $cat ( keys %cat_hash ) {

    #         my $rc_cat = arXiv::Categories::reverse_canonicalize_category($cat);
    #         if ($rc_cat ne $cat
    #             and not($rc_cat ~~ @cat_list)) {
    #             push @cat_list, $rc_cat;
    #         }
    #     }
    #     my @new_cats = ( shift @cat_list, sort @cat_list );
    #     $cat_str =  join ' ', @new_cats;
    #     return $cat_str;
    # }


    @property
    def num_unique_secondaries(self):        
    # # return number of secondaries minus duplicates (aliased or subsumed categories)
    # sub num_unique_secondaries {
    #     my $self = shift;

    #     my @cats;
    #     my $secondaries = $self->secondaries;
    #     while ( my $cat = $secondaries->next ) {
    #         push @cats, $cat->category;
    #     }

    #     my $cat_obj = arXiv::Categories->new(join(' ', @cats));
    #     return scalar($cat_obj->minimal_list());
    # }



    def is_category_in_archives(self, cat):
        ...
    # # Is the supplied category in the existing archives for this object?
    # # - get the archives that the existing categories belong to
    # # - if the existing cateogry is a general category, set key's value to 2
    # # return 1 if supplied category is in one of the existing archives
    # # return 2 "" AND existing archive is represented by a general category
    # # otherwise return 0
    # sub is_category_in_archives {
    #     my ( $self, $cat ) = @_;

    #     my %existing_archives = ();
    #     while ( my $old_cat = $self->next ) {
    #         my $archive =
    #           arXiv::Categories::get_archive_from_category( $old_cat->category );
    #         $existing_archives{$archive} = 1;
    #         $existing_archives{$archive} = 2
    #           if ( arXiv::Categories::is_general_category( $old_cat->category ) );
    #     }    

    #     if ( $existing_archives{arXiv::Categories::get_archive_from_category($cat)} ) {
    #         return $existing_archives{arXiv::Categories::get_archive_from_category($cat)};
    #     }

    #     return 0;
    # }


    # this isn't really useful in python
    def is_category_in_categories(self, cat):
        ...
    # sub is_category_in_categories {
    #     my ( $self, $cat ) = @_;

    #     return ( $self->search( { category => $cat } )->count > 0 ? 1 : 0 );
    # }


