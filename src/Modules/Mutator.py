#!/usr/bin/python

"""
    Module for mutating a string.

    Mutations are described in the original coordinates. These coordinates are
    transfered to the mutated coordinates with the aid of an internal shift
    list, which keeps track of the sizes of changes. Using the original
    coordinates greatly simplifies combined mutations in a variant.

    The original as well as the mutated string are stored.

    Public classes:
        Mutator ; Mutate a string and register all shift points.
"""

class Mutator() :
    """
        Mutate a string and register all shift points.

        Private variables:
            __shift ; A sorted list of tuples (position, shiftsize) where the
                      modifications in length are stored. Each first element of
                      the tuples in this list is unique, each second element is
                      non-zero.

        Public variables:
            orig    ; The original string.
            mutated ; The mutated string.
        
        Special methods:
            __init__(orig) ; Initialise the class with the original string.
        
        Private methods:
            __sortins(tuple)      ; Insert a tuple in a sorted list, after 
                                    insertion the list stays sorted.
            __mutate(pos1, pos2, ins) ; A general mutation function that does a
                                        delins on interbase coordinates of the 
                                        original string.

        Public methods:
            shiftpos(position)       ; Calculate the position in the mutated 
                                       string given the position in the 
                                       original string.
            newSplice(sites)         ; Generate a list of new splice sites.
            delM(pos1, pos2)         ; Delete a range from non-interbase 
                                       position pos1 to pos2.
            insM(pos, ins)           ; Insert a string at interbase position 
                                       pos.
            delimsM(pos1, pos2, ins) ; Delete a range from non-interbase 
                                       position pos1 to pos2 and insert ins.
            subM(pos, nuc)           ; Substitute a nucleotite at non-interbase
                                       position pos for nuc.
            invM(pos1, pos2)         ; Invert a range from non-interbase 
                                       position pos1 to pos2.
            dupM(pos1, pos2)         ; Duplicate a range from non-interbase 
                                       position pos1 to pos2.
    """

    def __init__(self, orig, config, output) :
        """
            Initialise the class with the original string.

            Arguments:
                orig   ; The original string before mutation.
                config ; Configuration variables.
                output ; The output object.

            Private variables (altered):
                __config ; Initialised with the configuration variables.
                __output ; Initialised with the output object.
                __shift  ; Initialised to the empty list.

            Public variables (altered):
                orig    ; Initialised to the parameter orig.
                mutated ; Initialised to the parameter orig.
        """

        self.__config = config
        self.__output = output
        self.__shift = []

        self.orig = orig
        self.mutated = orig
    #__init__
    
    def __sortins(self, tuple) :
        """
            Insert a tuple in a sorted list, the list is sorted on the first
            element of the tuples. After insertion the list stays sorted.
            If a tuple is inserted where tuple[0] already exists, this entry
            is altered.
            If an altered entry has zero as its second element, the entry is
            removed.

            Arguments:
                tuple ; An ordered pair where tuple[0] denotes a position and
                        tuple[1] denotes the change in shift at this position.

            Private variables (altered):
                __shift ; A tuple can be added, removed or altered.
        """
        if not tuple[1] : # Only non-zero shift sizes are relevant.
            return

        for i in range(len(self.__shift)) : # Look where to insert this tuple
            if self.__shift[i][0] == tuple[0] : # If it already exists, 
                self.__shift[i][1] += tuple[1]  # alter it.
                if not self.__shift[i][1] :     # If it results in a zero,
                    self.__shift.pop(i)         # remove it.
                return
            #if

            if self.__shift[i][0] > tuple[0] : # We found a successor, so 
                self.__shift.insert(i, tuple)  # insert it before the successor.
                return
            #if
        #for
    
        self.__shift.append(tuple) # If we couldn't find a successor, so this 
                                   # entry will be the last one in the list.
    #__sortins
    
    def __mutate(self, pos1, pos2, ins) :
        """
            A general mutation function that does a delins on interbase 
            coordinates of the original string. The change in length (if any) 
            is stored by calling the __sortins() function.
            The coordinates are those of the original string, so we use the
            __shifsize() function to map them to the mutated string, on which
            we perform the alteration.
            
            Arguments:
                pos1 ; The first interbase position of the deletion.
                pos2 ; The second interbase position of the deletion.
                ins  ; The insertion.

            Private variables:
                __config ; The variables maxvissize, flanksize and flankclipsize
                           are used in the visualisation.
                __output ; Visualisation information is added.

            Public variables (altered):
                mutated ; This string will reflect the result of the given 
                          delins.
        """

        # This part is just a visualisation, needs more attention.
        #

        loflank = self.orig[max(pos1 - self.__config.flanksize, 0):pos1]
        roflank = self.orig[pos2:pos2 + self.__config.flanksize]
        odel = self.orig[pos1:pos2]
        if len(odel) > self.__config.maxvissize :
            odel = "%s [%ibp] %s" % (odel[:self.__config.flankclipsize], 
                len(odel) - self.__config.flankclipsize * 2,
                odel[-self.__config.flankclipsize:])

        bp1 = self.shiftpos(pos1)
        bp2 = self.shiftpos(pos2)
        lmflank = self.mutated[max(bp1 - self.__config.flanksize, 0):bp1]
        rmflank = self.mutated[bp2:bp2 + self.__config.flanksize]

        insvis = ins
        if len(ins) > self.__config.maxvissize :
            insvis = "%s [%ibp] %s" % (ins[:self.__config.flankclipsize],
                len(ins) - self.__config.flankclipsize * 2,
                ins[-self.__config.flankclipsize:])
        fill = abs(len(odel) - len(insvis))
        if len(odel) > len(ins) :
            self.__output.addOutput("visualisation", 
                                  "%s %s %s" % (loflank, odel, roflank))
            self.__output.addOutput("visualisation",
                                  "%s %s%s %s" % (lmflank, insvis, '-' * fill, 
                                                  rmflank))
        #if
        else :
            self.__output.addOutput("visualisation",
                                  "%s %s%s %s" % (loflank, odel, '-' * fill, 
                                                  roflank))
            self.__output.addOutput("visualisation",
                                        "%s %s %s" % (lmflank, insvis, rmflank))
        #else

        #
        # End visualisation part.

        self.mutated = self.mutated[:self.shiftpos(pos1)] + ins + \
                       self.mutated[self.shiftpos(pos2):]
        self.__sortins([pos1 + 1, len(ins) + pos1 - pos2])
    #__mutate

    def shiftpos(self, position) :
        """
            Calculate the position in the mutated string, given a position in
            the original string. 

            Arguments:
                position ; The position in the original string for which we 
                           want the shift size.

            Private variables:
                __shift ; Used to calculate the shift.
            
            Returns:
                integer ; The position in the mutated string.
        """
        ret = position
    
        for i in range(len(self.__shift)) :
            if self.__shift[i][0] > position :
                return ret

            ret += self.__shift[i][1]
        #for
    
        return ret
    #shiftpos
    
    def newSplice(self, sites) :
        """
            Generate a list of new splice sites.

            Arguments:
                sites ; A list of old splice sites.

            Returns:
                list ; A list of new splice sites.
        """

        ret = []

        j = 0
        for i in sites :
            if (j % 2) :
                ret.append(self.shiftpos(i + 1) - 1)
            else :
                ret.append(self.shiftpos(i - 1) + 1)
            j += 1

        return ret
    #newSplice
    
    def delM(self, pos1, pos2) :
        """
            Delete a range from non-interbase position pos1 to pos2.

            Arguments:
                pos1 ; The first nucleotide of the range to be deleted.
                pos2 ; The last nucleotide of the range to be deleted.

            Private variables:
                __output ; Visualisation information is added.
        """

        if pos1 == pos2 :
            self.__output.addOutput("visualisation", "deletion of %i" % pos1)
        else :
            self.__output.addOutput("visualisation", "deletion of %i to %i" % (
                                    pos1, pos2))
        self.__mutate(pos1 - 1, pos2, '')
    #delM
    
    def insM(self, pos, ins) :
        """
            Insert a string at interbase position pos.

            Arguments:
                pos ; The interbase position where the insertion should take
                      place.
                ins ; The insertion, a string.

            Private variables:
                __output ; Visualisation information is added.
        """

        self.__output.addOutput("visualisation", 
                                "insertion between %i and %i" % (pos, pos + 1))
        self.__mutate(pos, pos, ins)
    #insM
    
    def delinsM(self, pos1, pos2, ins) :
        """
            Delete a range from non-interbase position pos1 to pos2 and insert 
            ins.

            Arguments:
                pos1 ; The first nucleotide of the range to be deleted.
                pos2 ; The last nucleotide of the range to be deleted.
                ins  ; The insertion, a string.
        """

        self.__mutate(pos1 - 1, pos2, ins)
    #delinsM
    
    def subM(self, pos, nuc) :
        """
            Substitute a nucleotite at non-interbase position pos for nuc.

            Arguments:
                pos ; The position where the substitution should take place.
                nuc ; The new nucleotide.

            Private variables:
                __output ; Visualisation information is added.
        """

        self.__output.addOutput("visualisation", "substitution at %i" % pos)
        self.__mutate(pos - 1, pos, nuc)
    #subM
    
    def invM(self, pos1, pos2) :
        """
            Invert a range from non-interbase position pos1 to pos2.

            Arguments:
                pos1 ; The first nucleotide of the range to be inverted.
                pos2 ; The last nucleotide of the range to be inverted.

            Public variables:
                orig ; The original string.
        """

        from Bio.Seq import reverse_complement # reverse_complement()

        self.__mutate(pos1 - 1, pos2, \
                      reverse_complement(self.orig[pos1 - 1:pos2]))
    #invM

    def dupM(self, pos1, pos2) :
        """
            Duplicate a range from non-interbase position pos1 to pos2.

            Arguments:
                pos1 ; The first nucleotide of the range to be duplicated.
                pos2 ; The last nucleotide of the range to be duplicated.

            Public variables:
                orig ; The original string.
        """

        self.__mutate(pos2, pos2, self.orig[pos1 - 1:pos2])
    #dupM
#Mutator

#
# Unit test.
#
if __name__ == "__main__" :
    pass
#if
